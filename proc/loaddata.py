#!/usr/bin/python
# !coding: utf-8

import os
import sys
import json
import textwrap
import optparse
import logging.config
from datetime import datetime
import unicodedata
import re

from pyramid.settings import aslist
from xylose.scielodocument import Article

from citedby import utils
from citedby.controller import controller, articlemeta

logger = logging.getLogger(__name__)

config = utils.Configuration.from_env()
settings = dict(config.items())

# set logger
logger = logging.getLogger('pcitations')

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def remove_accents(text):
    nfkd_form = unicodedata.normalize('NFKD', text.strip())
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def citation_meta(document):
    """
    This function receives a article meta JSON, transform it in an citation
    dicitionary, look the response example.

    :param document: ArticleMeta Xylose Document

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

    if document.citations:

        c_dict = {}

        c_dict['titles'] = []
        c_dict['url'] = document.html_url()
        c_dict['issn'] = document.journal.scielo_issn
        c_dict['pid'] = document.publisher_id
        c_dict['code'] = document.publisher_id
        c_dict['collection'] = document.collection_acronym
        c_dict['document_type'] = document.document_type

        if document.doi:
            c_dict['doi'] = document.doi

        if document.journal.title:
            c_dict['source'] = document.journal.title

        if document.translated_titles():
            c_dict['titles'] = [t for l, t in document.translated_titles().items() if t != None]

        if document.original_title():
            c_dict['titles'].append(document.original_title())

        if document.authors:
            c_dict['authors'] = document.authors

        if document.subject_areas:
            c_dict['subject_areas'] = document.subject_areas

        if document.first_author:
            c_dict['first_author'] = document.first_author

        if document.start_page:
            c_dict['start_page'] = document.start_page

        if document.end_page:
            c_dict['end_page'] = document.end_page

        if document.publication_date:
            c_dict['publication_year'] = document.publication_date[:4]

        for cit in document.citations:

            if cit.source:
                c_dict['reference_source'] = cit.source
                c_dict['reference_source_cleaned'] = remove_tags(remove_accents(cit.source)).lower()

            if cit.title():
                c_dict['reference_title'] = cit.title()
            elif cit.chapter_title:
                c_dict['reference_title'] = cit.chapter_title

            if cit.date:
                c_dict['reference_publication_year'] = cit.date[:4]

            if cit.authors:
                c_dict['reference_authors'] = cit.authors

            if cit.first_author:
                c_dict['reference_first_author'] = ' '.join([
                    cit.first_author.get('given_names', ''),
                    cit.first_author.get('surname', '')
                ])

            if cit.start_page:
                c_dict['reference_start_page'] = cit.start_page

            if cit.end_page:
                c_dict['reference_end_page'] = cit.end_page

            if cit.end_page:
                c_dict['reference_index_number'] = str(cit.index_number)

            c_dict['_id'] = '-'.join([
                document.collection_acronym,
                document.publisher_id,
                str(cit.index_number)
            ])

            yield c_dict

class PCitation(object):
    """
    Process citation getting articles from Article Meta
    """

    usage = """\
    %prog -f (full) index all citations OR -d (distinct) only difference
    between endpoints.

    This process collects all articles in the Article meta
    http://articlemeta.scielo.org and index in ES (elasticsearch).

    With this process it is possible to process all the citations or only difference
    between elasticsearch and Article Meta, use pcitations -h to verify the options list.

    Edit logging.ini to change logging definitions.
    """

    parser = optparse.OptionParser(
        textwrap.dedent(usage), version="prog 0.9 - beta")

    parser.add_option('-f', '--full', action='store_true',
                      help='update all documents and insert the difference')

    parser.add_option('-r', '--rebuild_index', action='store_true',
                      help='this will remove all data in ES and\
                             index all documents')

    parser.add_option('-o', '--offset', action='store', default=5000,
                      help='Bulk offset, default= 5000')

    def __init__(self, argv):
        self.started = None
        self.finished = None
        self.options, self.args = self.parser.parse_args(argv)

        hosts = aslist(settings['app:main'].get('elasticsearch_host', '127.0.0.1:9200'))
        index = settings['app:main'].get('elasticsearch_index', 'citations')

        self.controller = controller(
            hosts=hosts,
            timeout=60,
            sniff_on_start=True,
            sniff_on_connection_fail=True
        )

        self.articlemeta = articlemeta()

    def _duration(self):
        """
        Return datetime process duration
        """
        return self.finished - self.started

    def _string_json(self, data):
        """
        Method convert string to json handler some errors.

        :param data: string

        :returns: json
        """

        try:
            jdata = json.loads(data)
        except ValueError as e:
            logger.error(e)
        else:
            return jdata

    def _bulk(self, documents):

        for document in documents:
            for reference in citation_meta(document):
                self.controller.index_citation(reference, reference['_id'])

    def run(self):
        """
        Run the Loaddata switching between full and incremental indexation
        """

        self.started = datetime.now()

        logger.info('Load Data Script (index citation)')

        logger.info('Get all ids from articlemeta')

        self.controller.load_mapping()

        documents = self.articlemeta.documents()

        if self.options.full:
            logger.info('You have selected full processing... this will take a while')

            if self.options.rebuild_index:
                logger.info('This will remove EVERYTHING from your search index')

                self.controller.index_reset()

            self._bulk(documents)

        else:
            logger.info('You have selected incremental processing...')
            self._bulk(documents)

        self.finished = datetime.now()

        logger.info("Total processing time: %s sec." % self._duration())


def main(argv=sys.argv[1:]):

    command = PCitation(argv)

    return command.run()