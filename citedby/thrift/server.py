#! /usr/bin/env python
# coding: utf-8

import os
import json
import logging

import thriftpy
import thriftpywrap

from pyramid.settings import aslist

from citedby.controller import controller, ServerError
from citedby.controller import cache_region as controller_cache_region
from citedby import utils

citedby_thrift = thriftpy.load(os.path.join(os.path.dirname(
                               os.path.abspath(__file__)), 'citedby.thrift'))

logger = logging.getLogger(__name__)


class Dispatcher(object):

    def __init__(self):

        config = utils.Configuration.from_env()
        settings = dict(config.items())

        es = os.environ.get(
            'ELASTICSEARCH_HOST',
            settings['app:main'].get('elasticsearch_host', '127.0.0.1:9200')
        )

        es_index = os.environ.get(
            'ELASTICSEARCH_INDEX',
            settings['app:main'].get('elasticsearch_index', 'citations')
        )

        self._controller = controller(
            hosts=aslist(es),
            timeout=600,
            sniff_on_connection_fail=True
        ).set_base_index(index=es_index)

        memcached_host = os.environ.get(
            'MEMCACHED_HOST',
            settings['app:main'].get('memcached_host', None)
        )

        memcached_expiration_time = os.environ.get(
            'MEMCACHED_EXPIRATION_TIME',
            settings['app:main'].get('memcached_expiration_time', 2592000)  # a month cache
        )

        ## Cache Settings Config
        if 'memcached_host' in settings['app:main']:
            cache_config = {}
            cache_config['expiration_time'] = int(memcached_expiration_time) # a month cache
            cache_config['arguments'] = {'url': memcached_host, 'binary': True}
            controller_cache_region.configure('dogpile.cache.pylibmc', **cache_config)
        else:
            controller_cache_region.configure('dogpile.cache.null')

    def search(self, body, parameters):

        params = {i.key: i.value for i in parameters}
        params['doc_type'] = 'citation'
        params['body'] = json.loads(body)

        try:
            data = self._controller.bibliometric_search(params)
        except ValueError as e:
            logging.error(e.message)
            raise citedby_thrift.ValueError(message=e.message)
        except ServerError as e:
            raise citedby_thrift.ServerError(message=e.message)

        try:
            data_str = json.dumps(data)
        except ValueError as e:
            logging.error('Invalid JSON data: %s', data_str)
            raise citedby_thrift.ValueError(message=e.message)

        return data_str

    def citedby_pid(self, query, metaonly):
        try:
            return json.dumps(
                self._controller.query_by_pid(query, metaonly=metaonly)
            )
        except Exception as e:
            logger.exception(e)
            raise citedby_thrift.ServerError(
                'Server Error: controller.query_by_pid(%s, %s)'
                % (query, metaonly)
            )

    def citedby_doi(self, query, metaonly):
        try:
            return json.dumps(
                self._controller.query_by_doi(query, metaonly=metaonly)
            )
        except Exception as e:
            logger.exception(e)
            raise citedby_thrift.ServerError(
                'Server Error: controller.query_by_doi(%s, %s)'
                % (query, metaonly)
            )

    def citedby_meta(self, title, author_surname, year, metaonly):
        try:
            return json.dumps(
                self._controller.query_by_meta(
                    title, author_surname, year, metaonly=metaonly)
            )
        except Exception as e:
            logger.exception(e)
            raise citedby_thrift.ServerError(
               'Server Error: controller.citedbymeta(%s, %s, %s, %s)'
               % (title, author_surname, year, metaonly)
            )

main = thriftpywrap.ConsoleApp(citedby_thrift.Citedby, Dispatcher)