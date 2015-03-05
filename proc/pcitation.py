#!/usr/bin/python
#coding: utf-8

import sys
import textwrap
import optparse
import logging.config
from datetime import datetime
from progressbar import ProgressBar

from xylose.scielodocument import Article

import articlemeta
from citedby.icitation import ICitation

# config logger file
logging.config.fileConfig('logging.ini')

# set logger
logger = logging.getLogger('pcitations')


def citation_meta(art_meta_json):
    """
    This function receives a article meta JSON, transform it in an citation
    dicitionary, look the response example.

    :param art_meta_json: Article Meta JSON

    This function only create keys that has content, ignore otherwise.

    :returns:
        {
          "url": "<DOAMIN>scielo.php?script=sci_arttext&pid=S0101-31222002000100038",
          "source": "Revista Brasileira de Sementes",
          "issn": "0101-3122",
          "code": "S0101-31222002000100038",
          "collection": "scl",
          "titles": ["Adequação do...", "Seconde title..."]
          "first_author": {role: "ND",
                           xref: ["A01"],
                           surname: "Moreira",
                           given_names: "Jessica Pronestino de Lima"},
          "publication_year": "2013",
          "citations":
          [{
              "source": "Anais da Academia Brasileira de Ciências",
              "first_author": "Moreira JK",
              "title": "Germination of Croton...",
              "publication_year": "2004"
           }]
        }
    """
    art = Article(art_meta_json)

    c_dict = {}

    #List of titles
    c_dict['titles'] = []

    c_dict['url'] = art.html_url()
    c_dict['source'] = art.journal.title
    c_dict['issn'] = art.journal.scielo_issn
    c_dict['code'] = art.publisher_id
    c_dict['id'] = '%s_%s' % (art.collection_acronym, art.publisher_id)

    if art.translated_titles():
        c_dict['titles'] = [t for l, t in art.translated_titles().items() if t != None]

    c_dict['titles'].append(art.original_title())
    c_dict['collection'] = art.collection_acronym
    c_dict['first_author'] = art.first_author

    if art.publication_date:
        c_dict['publication_year'] = art.publication_date[:4]

    if art.citations:

        art_citations = []

        for cit in art.citations:
            ac_dict = {}
            ac_dict['source'] = cit.source

            if cit.title():
                ac_dict['title'] = cit.title()
            elif cit.chapter_title:
                ac_dict['title'] = cit.chapter_title

            if cit.date:
                ac_dict['publication_year'] = cit.date[:4]

            ac_dict['first_author'] = cit.first_author

            art_citations.append(ac_dict)

        c_dict['citations'] = art_citations

    return c_dict


class PCitation(object):
    """
    Process citation getting articles from Article Meta
    """

    usage = """\
    %prog -f (full) index all citations OR -d (distiction) only difference
    between endpoints.

    This process collects all articles in the Article meta
    http://articlemeta.scielo.org and index in ES (elasticsearch).

    With this process it is possible to process all the citations or only difference
    between elasticsearch and Article Meta, use pcitations -h to verify the options list.

    Edit logging.ini to change logging definitions.
    """

    parser = optparse.OptionParser(textwrap.dedent(usage),
                                    version="%prog 0.9 - beta")

    parser.add_option('-f', '--full', action='store_true',
                        help='update all documents and insert the difference')

    parser.add_option('-d', '--distiction', action='store_true',
                        help='index only difference between endpoints\
                             (Article Meta and Elasticsearch Citation)')

    parser.add_option('-r', '--rebuild_index', action='store_true',
                        help='this will remove all data in ES and\
                             index all documents')

    parser.add_option('-l', '--list_hosts', action='store',
                        help='list of ES hosts, Ex.: esa.scielo.org esb.scielo.org,\
                        default is localhost')

    def __init__(self, argv):
        self.started = None
        self.finished = None
        self.options, self.args = self.parser.parse_args(argv)

    def _duration(self):
        """
        Return datetime process duration
        """
        return self.finished - self.started

    def _checkparam(self):
        """
        Return a Boolean checking the params
        """
        ret = True

        if not (self.options.full or self.options.distiction or self.options.rebuild_index):
            self.parser.error('One of params -f (full), -d (distiction) or -r (rebuild_index) must be used.')
            ret = False

        if self.options.full and self.options.distiction:
            self.parser.error("options -d and -f are mutually exclusive.")
            ret = False

        return ret

    def _difflist(first_list, second_list):
        """
        Difference between two list

        :param first_list: First list for compare
        :param second_list: Second list for compare

        :returns: list of difference
        """
        return list(set(first_list) - set(second_list))

    def run(self):
        """
        Run the PCitation switching between full and partial indexation
        """

        self.started = datetime.now()

        if not self._checkparam():
            return None

        logger.info('Start PCitation Script (Index citation)')

        meta_total = articlemeta.get_identifiers_count()

        logger.info('Total of items in Article Meta: %d' % meta_total)

        icitation = ICitation(hosts=self.options.list_hosts)

        cite_total = icitation.count_citation()

        logger.info('Total of items indexed in ES Index Citation: %d' % cite_total)

        logger.info('Get identifiers from Article Meta...')

        meta_idents = []
        with ProgressBar(maxval=meta_total) as progress:
            for ident in articlemeta.get_all_identifiers():
                meta_idents.append(ident)
                progress.update(len(meta_idents))

        if self.options.distiction:

            logger.info('You select distinct processing, get identifiers from ES Index Citation...')

            es_idents = icitation.get_identifiers()

            #Itens that will be index (A-B)
            idents = self._difflist(meta_idents, es_idents)
            logger.info('Total itens that will be index: %s' % len(idents))

            #Remove itens (B-A)
            remove_idents = self._difflist(es_idents, meta_idents)
            logger.info('Total of items that will be remove from ES: %s' % len(remove_idents))
            if remove_idents: # if exists itens to remove
                with ProgressBar(maxval=len(remove_idents)) as progress:
                    for i, ident in enumerate(remove_idents):
                        icitation.del_citation(ident)
                        progress.update(i)

        elif self.options.full:
            logger.info('You select full processing... this will take a while')
            idents = meta_idents

        elif self.options.rebuild_index:
            logger.info('You select Rebuild Index processing, deleting %d items in Index Citation.' % cite_total)
            logger.info('WARNING: This will remove EVERYTHING from your search index')
            icitation.del_all_citation()
            idents = meta_idents

        logger.info('Index citations...')

        if idents:
            with ProgressBar(maxval=len(idents)) as progress:
                for i, ident in enumerate(idents):
                    c_meta_dict = citation_meta(articlemeta.get_article(*ident))
                    icitation.index_citation(c_meta_dict)
                    progress.update(i)

        self.finished = datetime.now()

        logger.info("Total processing time: %s sec." % self._duration())


def main(argv=sys.argv[1:]):

    command = PCitation(argv)

    return command.run()


if __name__ == "__main__":

    # command line
    sys.exit(main() or 0)
