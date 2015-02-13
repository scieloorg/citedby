#!/usr/bin/python
#coding: utf-8
import sys
import csv
import optparse
import textwrap
import requests

from citedby.icitation import ICitation


def _fetch_data(self, resource):
    """
    Fetches any resource.

    :param resource: any resource
    :returns: requests.response object
    """
    try:
        response = requests.get(resource)
    except requests.exceptions.RequestException as e:
        print '%s. Unable to connect to resource.' % e
    else:
        print 'Get resource: %s' % resource

        return response


def main():

    usage = """\
    %prog this script get all identifiers and save it on 'identifiers.txt'
    """

    parser = optparse.OptionParser(textwrap.dedent(usage),
                                    version="%prog 0.1 - beta")

    parser.add_option('-l', '--list_hosts', action="store",
                        help='list of ES hosts, Ex.: esa.scielo.org esb.scielo.org,\
                        default is localhost')

    options, args = parser.parse_args(sys.argv)

    icitation = ICitation(hosts=options.list_hosts)

    total = icitation.count_citation()

    print 'Total of article in ES Citation: %s' % total

    print 'Get identifiers from ES Index Citation...this will take a while!'

    #('acronym of collection', SciELO PID)
    es_idents = icitation.get_identifiers()

    fp = open('identifiers.txt', 'a')

    writer = csv.writer(fp, delimiter='|', quotechar='"')

    for ident in es_idents:
        writer.writerow([ident[1], ident[0]])

    fp.close()

if __name__ == "__main__":
    main()


