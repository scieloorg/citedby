#!/usr/bin/python
#coding: utf-8


import os.path
import time
import sys
import csv
import json
import textwrap
import optparse
import logging.config
from datetime import datetime

import requests
from citedby.icitation import ICitation


class CCitation(object):
    """
    Count citation
    """

    usage = """\
    %prog this count how many articles have citation in SciELO
    """

    parser = optparse.OptionParser(textwrap.dedent(usage),
                                    version="%prog 0.9 - beta")

    parser.add_option('-o', '--output_file', action="store", type="string",
                        help='path to output csv file content result of process')

    parser.add_option('-l', '--list_hosts', action="store",
                        help='list of ES hosts, Ex.: esa.scielo.org esb.scielo.org,\
                        default is localhost, it use to create the identifiers.txt file.')


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

        if not self.options.output_file or not self.options.list_hosts:
            self.parser.error('parm -o (output_file) must be used and -l list of ES hosts')
            return False

        return True


    def _fetch_data(self, resource):
        """
        Fetches any resource, this will try to get the resource if doesnt work
        it will try infinitely sleep 10 seconds between attempts

        :param resource: any resource
        :returns: requests.response object
        """
        try:
            response = requests.get(resource)
        except requests.exceptions.RequestException as e:
            logger.error('Unable to connect to resource. %s' % e)

            while True:
                try:
                    logger.info('Try to get the resource again: {0}'.format(resource))
                    return requests.get(resource)
                except requests.exceptions.RequestException as e:
                    logger.error('Sleep for 10 second to try again: {0}'.format(resource))
                    time.sleep(10)

        else:
            logger.debug('Get resource: %s' % resource)

            return response


    def _file_identifiers(self, filename, idents):
        """
        This method will generate a file system content all identifiers
        provide from ES citation index.
        """

        fp = open(filename, 'a')

        writer = csv.writer(fp, delimiter='|', quotechar='"')

        logger.info('Get identifiers from ES Index Citation...this will take a while!')

        for ident in idents:
            writer.writerow([ident[1], ident[0]])

        fp.close()


    def run(self):

        self.started = datetime.now()

        if not self._checkparam():
            return None

        logger.info('Start Count Citation Script')

        icitation = ICitation(hosts=self.options.list_hosts)

        total_citation = icitation.count_citation()

        logger.info('Total of article in ES Citation: %s' % total_citation)

        #if identifiers dont exists create and read to get all identifiers
        if os.path.exists('identifiers.txt'):
            fp = open('identifiers.txt', 'r')
            es_idents = fp.readlines()
        else:
            self._file_identifiers('identifiers.txt', icitation.get_identifiers())
            fp = open('identifiers.txt', 'r')
            es_idents = csv.reader(fp, delimiter='|', quotechar='"')

        #create a csv file with result
        f = open(self.options.output_file, 'ab')

        writer = csv.writer(f, delimiter='|', quotechar='"')
        count = 0

        #loop all identifiers from ES
        for row in es_idents:
            ident = row.split('|')[0]
 
            response = self._fetch_data('http://citedby.scielo.org/api/v1/pid/?q=%s' % ident)

            if response.status_code == 200:

                citation = json.loads(response.text)

                #add in csv file only articles with citations
                if len(citation['cited_by']) > 0:
                    writer.writerow([ident, str(len(citation['cited_by']))])
                    count +=1 

        writer.writerow(['Total of articles with current citation', str(count)])

        f.close()

        self.finished = datetime.now()

        logger.info("Total processing time: %s sec." % self._duration())


def main(argv=sys.argv[1:]):

    command = CCitation(argv)

    return command.run()


if __name__ == "__main__":

    # config logger file
    logging.config.fileConfig('logging.ini')

    # set logger
    logger = logging.getLogger('ccitation')

    # command line
    sys.exit(main() or 0)
