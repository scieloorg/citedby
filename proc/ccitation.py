#!/usr/bin/python
#coding: utf-8

import sys
import textwrap
import optparse
import logging.config
from datetime import datetime

import requests
from citedby.icitation import ICitation


class CCitation(object):
    """
    Cheking Citation against SciELO Site
    """

    usage = """\
    %prog this script search the citation on Elasticsearch and verify if the
    citation exists in OnLine Site http://www.scielo.br
    """

    parser = optparse.OptionParser(textwrap.dedent(usage),
                                    version="%prog 0.9 - beta")
    parser.add_option('-p', '--phrase', action="append",
                        help='phrase to be search on citation index (multiple -p args accepted)')
    parser.add_option('-a', '--author_surname', action='store',
                        help='the author surname')
    parser.add_option('-y', '--publication_year', action='store',
                        help='publication year of the article')

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

        if not (self.options.phrase or self.options.author_surname or self.options.publication_year):
            self.parser.error('One of params -p (phrase), -a (author surname) or -y (publication year) must be used.')
            return False

        return True


    def _format_citation(self, citations):
        """
        Format the citation like:
            [{
                url: "http://www.scielo.cl/scielo.php?script=sci_arttext&pid=S0716-10182009000100012&lng=en&tlng=en",
                source: "Revista chilena de infectología",
                issn: "0716-1018",
                code: "S0716-10182009000100012",
                title: "Fiebre tifoidea en Santiago, Chile y su control"
            }]
        """
        l = []

        for citation in citations['hits']['hits']:
            l.append({
                    'titles': citation['_source']['titles'],
                    'url': citation['_source']['url'],
                    'code': citation['_source']['code'],
                    'source': citation['_source']['source'],
                    'issn': citation['_source']['issn']})
        return l


    def _fetch_data(self, resource):
        """
        Fetches any resource.

        :param resource: any resource
        :returns: requests.response object
        """
        try:
            response = requests.get(resource)
        except requests.exceptions.RequestException as e:
            logger.error('%s. Unable to connect to resource.' % e)
        else:
            logger.debug('Get resource: %s' % resource)

            return response


    def run(self):

        self.started = datetime.now()

        if not self._checkparam():
            return None

        logger.info('Start Check Citation Script\n')

        icitation = ICitation()

        citations = self._format_citation(icitation.search_citation(
                                          titles=self.options.phrase,
                                          author_surname=self.options.author_surname,
                                          year=self.options.publication_year))

        print u"Encontrado %s artigo(s) que citam o(s) título(s): %s\n" % (len(citations), self.options.phrase)

        error_list = []
        for citation in citations:

            print "#" * 80

            f_data = self._fetch_data(citation['url'])

            if unicode(self.options.phrase) in f_data.text:
                print u"Existe title: %s in %s" % (self.options.phrase, citation['url'])
            else:
                error_list.append(citation['url'])

            print "#" * 80 + "\n"

        if error_list:
            print u"%d iten(s) não foram encontrado para a frase: '%s', verifique manualmente:\n" % (len(error_list), self.options.phrase)

            print 'Frases: %s\n' % '\n\t'.join(self.options.phrase)
            print 'URL(s): %s\n' % '\n\t'.join(error_list)

        self.finished = datetime.now()

        logger.info("Total processing time: %s sec." % self._duration())


def main(argv=sys.argv[1:]):

    command = CCitation(argv)

    return command.run()


if __name__ == "__main__":

    # config logger file
    logging.config.fileConfig('logging.ini')

    # set logger
    logger = logging.getLogger('pcitations')

    # command line
    sys.exit(main() or 0)
