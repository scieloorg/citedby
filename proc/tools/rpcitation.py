#!/usr/bin/python
#coding: utf-8

import sys
import textwrap
import optparse
import logging.config
from datetime import datetime
from progressbar import ProgressBar


from citedby.icitation import ICitation


class RPCitation(object):
    """
    Rebuild citation getting articles from ``citations`` index.
    """

    usage = """\
    %prog rebuild all citations

    This process collects all articles in ``citations`` index and rebuild in target
    index.
    """

    parser = optparse.OptionParser(textwrap.dedent(usage),
                                    version="%prog 0.9 - beta")

    parser.add_option('-f', '--source_index', action='store',
                        help='new content that will receive the reconstructed data')

    parser.add_option('-t', '--target_index', action='store',
                        help='new content that will receive the reconstructed data')


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

        if not self.options.source_index and not self.options.target_index:
            self.parser.error('-f and -t are required')
            return False

        return True

    def _get_meta(self, data):
        """
        Get meta from ``_source`` of Elasticsearch response.
        """
        return data['_source']

    def run(self):
        """
        Run the RPCitation to rebuild index
        """
        if not self._checkparam():
            return None

        self.started = datetime.now()

        logger.info('Start RPCitation Script (R-Index citation)')

        icitation = ICitation(hosts=self.options.source_index)

        cite_total = icitation.count_citation()

        logger.info('Total of itens that will be re-index on ``%s``: %d' % (self.options.target_index, cite_total))

        ricitation = ICitation(hosts=self.options.target_index)

        with ProgressBar(maxval=cite_total) as progress:
            for index, cite in enumerate(icitation.get_all()):
                ricitation.index_citation(self._get_meta(cite))
                progress.update(index)

        self.finished = datetime.now()

        logger.info("Total processing time: %s sec." % self._duration())


def main(argv=sys.argv[1:]):

    command = RPCitation(argv)

    return command.run()


if __name__ == "__main__":

    # config logger file
    logging.config.fileConfig('logging.ini')

    # set logger
    logger = logging.getLogger('pcitations')

    # command line
    sys.exit(main() or 0)
