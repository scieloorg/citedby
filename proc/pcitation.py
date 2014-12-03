#!/usr/bin/python
#coding: utf-8

import sys
import textwrap
import optparse
import logging.config
from datetime import datetime
from progressbar import ProgressBar

import utils
from citedby.icitation import ICitation


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
    """
    default_verbosity = 1

    parser = optparse.OptionParser(textwrap.dedent(usage),
                                    version="%prog 0.9 - beta")

    parser.add_option('-f', '--full', action='store_true',
                        help='index all documents')

    parser.add_option('-d', '--distiction', action='store_true',
                        help='index only difference between endpoints\
                             (Article Meta and Elasticsearch Citation)')

    parser.add_option('-v', '--verbose', default=default_verbosity, dest='verbose',
        action='count', help="Set verbose level (default "+str(default_verbosity)+")")


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

        if not (self.options.full or self.options.distiction):
            self.parser.error('One of params -f (full) or -d (distiction) must be used')
            ret = False

        if self.options.full and self.options.distiction:
            self.parser.error("options -d and -f are mutually exclusive")
            ret = False

        return ret

    def run(self):
        """
        Run the PCitation switching between full and partial indexation
        """
        try:
            self.started = datetime.now()

            if not self._checkparam():
                return None

            logger.info('Start PCitation Script (Index citation)')

            meta_total = utils.get_identifiers_count()

            logger.info('Total of items in Article Meta: %d' % meta_total)

            icitation = ICitation()

            cite_total = icitation.count_citation()

            logger.info('Total of items indexed in ES Index Citation: %d' % cite_total)

            logger.info('Get identifiers from Article Meta...')

            with ProgressBar(maxval=utils.get_identifiers_count()) as progress:
                meta_idents = []
                for ident in utils.get_all_identifiers():
                    meta_idents.append(ident)
                    progress.update(len(meta_idents))

            if self.options.distiction:

                logger.info('You select distinct processing, get identifiers from ES Index Citation...')

                es_idents = icitation.get_identifiers()

                #Itens that will be index (A-B)
                idents = utils.diff_list(meta_idents, es_idents)
                logger.info('Total itens that will be index: %s' % len(idents))

                #Remove itens (B-A)
                remove_idents = utils.diff_list(es_idents, meta_idents)
                if remove_idents: # if exists itens to remove
                    with ProgressBar(maxval=len(remove_idents)) as progress:
                        for i, ident in enumerate(remove_idents):
                            icitation.del_citation(ident)
                            progress.update(i)

                logger.info('Total of items that will be remove from ES: %s' % len(remove_idents))
            else:
                logger.info('You select full processing, deleting %d items in Index Citation.' % cite_total)
                icitation.del_all_citation()
                idents = meta_idents

            logger.info('Index citations...')

            if idents:
                with ProgressBar(maxval=len(idents)) as progress:
                    for i, ident in enumerate(idents):
                        c_meta_dict = utils.citation_meta(utils.get_article(*ident))
                        icitation.index_citation(c_meta_dict)
                        progress.update(i)

            self.finished = datetime.now()

            logger.info("Total processing time: %s sec." % self._duration())

        except (SystemExit, KeyboardInterrupt) as e:
            if self.options.verbose > 1:
                raise
            logger.info('Exiting%s (-v to see traceback)' % e)


def main(argv=sys.argv[1:]):

    command = PCitation(argv)

    return command.run()


if __name__ == "__main__":

    # config logger file
    logging.config.fileConfig('config/logging.ini')

    # set logger
    logger = logging.getLogger('pcitations')

    # command line
    sys.exit(main() or 0)
