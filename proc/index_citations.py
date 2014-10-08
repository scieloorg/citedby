#!/usr/bin/python
#coding: utf-8

import json
import requests
import argparse
import ConfigParser
import logging.config


def get_identifiers(config, offset):

    url = '{0}?offset={4}'.format(config['endpoints']['identifiers'], offset)

    log.debug('URL used for retrieve identifiers list: {0}'.format(url))

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        log.critical('Connection error: {0}'.format(e))
    else:
        response_json = json.loads(response.text)
        return response_json['meta']['total'], list(response_json['objects'])


def main(config):

    indexer = config.get('endpoints', 'indexer')

    parser = argparse.ArgumentParser(
                        description='Script insert/update citation in %s' % indexer)

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-f', '--full',
                        action='store_true',
                        help='index all documents exist in %s' % indexer)

    group.add_argument('-d', '--distiction',
                        action='store_true',
                        help='index only documents that does not exist in %s' % indexer)

    parser.add_argument('-l', '--loglevel', dest="loglevel",
                        default=logging.INFO, help='set the log level')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 0.1')

    args = parser.parse_args()

    if args.loglevel:
        log.setLevel(args.loglevel)

    log.info('Start citation script')


if __name__ == "__main__":

    #config app file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config/config.ini'))

    # config logger file
    logging.config.fileConfig('config/logging.ini')

    # create logger
    log = logging.getLogger('index_citations')

    main(config)
