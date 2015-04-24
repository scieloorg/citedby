#! /usr/bin/env python
#coding: utf-8

import os
import json
import argparse
import thriftpy
from thriftpy.rpc import make_server
from ConfigParser import SafeConfigParser


from citedby.icitation import ICitation
from dogpile.cache import make_region
from citedby.icontroller import (query_by_pid,
                                 query_by_doi,
                                 query_by_meta)

from citedby.utils import key_generator

ADDRESS = '0.0.0.0'
PORT = '11610'

citedby_thrift = thriftpy.load(os.path.join(os.path.dirname(
                               os.path.abspath(__file__)), 'citedby.thrift'))

cache_region = make_region(name="citedby_trhift",
                           function_key_generator=key_generator)


class Dispatcher(object):

    def __init__(self, config_path):

        config = SafeConfigParser()
        config.readfp(open(config_path))

        self.settings = dict(config.items('app:main'))

        self.index = ICitation(
            hosts=self.settings['elasticsearch_host'].split())

        cache_region.configure('dogpile.cache.bmemcached',
            expiration_time=int(self.settings['memcached_expiration_time']),
            arguments={'url':self.settings['memcached_arguments_url'].split()})

    def citedby_pid(self, q, metaonly):

        @cache_region.cache_on_arguments(namespace=self.settings['memcached_prefix_thrift'])
        def _citedby_pid(q, metaonly):
            try:
                return json.dumps(query_by_pid(self.index, q, metaonly))
            except:
                return citedby_thrift.ServerError(
                                'Server Error: icontroller.query_by_pid(%s, %s, %s)'
                                 % (self.index, q, metaonly)).message

        return _citedby_pid(q, metaonly)

    def citedby_doi(self, q, metaonly):

        @cache_region.cache_on_arguments(namespace=self.settings['memcached_prefix_thrift'])
        def _citedby_doi(q, metaonly):
            try:
                return json.dumps(query_by_doi(self.index, q, metaonly))
            except:
                return citedby_thrift.ServerError(
                                'Server Error: icontroller.query_by_doi(%s, %s, %s)'
                                % (self.index, q, metaonly)).message

        return _citedby_doi(q, metaonly)

    def citedby_meta(self, title, author_surname, year, metaonly):

        @cache_region.cache_on_arguments(namespace=self.settings['memcached_prefix_thrift'])
        def _citedby_meta(title, author_surname, year, metaonly):
            try:
                return json.dumps(
                    query_by_meta(self.index, title, author_surname, year, metaonly))
            except:
                return citedby_thrift.ServerError(
                    'Server Error: icontroller.citedbymeta(%s, %s, %s, %s, %s)'
                     % (self.index, title, author_surname, year, metaonly)).message
        return _citedby_meta(title, author_surname, year, metaonly)


def main():

    parser = argparse.ArgumentParser(
        description="Citedby Thrift Server."
    )

    parser.add_argument(
        '--address',
        '-a',
        default=ADDRESS,
        help='Binding Address'
    )


    parser.add_argument(
        '--port',
        '-p',
        default=PORT,
        help='Binding Port'
    )

    parser.add_argument(
        '--config_path',
        '-c',
        default='production.ini',
        help='Config file path, default: production.ini'
    )

    args = parser.parse_args()

    server = make_server(citedby_thrift.Citedby,
        Dispatcher(args.config_path), args.address, args.port)
    server.serve()