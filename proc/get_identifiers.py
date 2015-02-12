#!/usr/bin/python
#coding: utf-8

import csv
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

    icitation = ICitation()

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


