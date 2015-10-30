#! /usr/bin/env python
# coding: utf-8

import os
import json
import argparse
from ConfigParser import SafeConfigParser

import thriftpy
import thriftpywrap

from pyramid.settings import aslist

from citedby.controller import controller, ServerError
from citedby import utils

citedby_thrift = thriftpy.load(os.path.join(os.path.dirname(
                               os.path.abspath(__file__)), 'citedby.thrift'))

class Dispatcher(object):

    def __init__(self):

        config = utils.Configuration.from_env()
        settings = dict(config.items())
        self._controller = controller(
            aslist(settings['app:main']['elasticsearch_host']),
            index=settings['app:main']['elasticsearch_index'],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            timeout=60
        )

    def search(self, body, parameters):

        params = {i.key:i.value for i in parameters}
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
            logging.error('Invalid JSON data: %s' % data_str)
            raise citedby_thrift.ValueError(message=e.message)

        return data_str

    def citedby_pid(self, q, metaonly):
        try:
            return json.dumps(
                self._controller.query_by_pid(q, metaonly)
            )
        except Exception as e:
            raise citedby_thrift.ServerError(
                'Server Error: icontroller.query_by_pid(%s, %s)'
                % (q, metaonly)
            )

    def citedby_doi(self, q, metaonly):
        try:
            return json.dumps(
                self._controller.query_by_doi(q, metaonly)
            )
        except:
            raise citedby_thrift.ServerError(
                'Server Error: icontroller.query_by_doi(%s, %s)'
                % (q, metaonly)
            )

    def citedby_meta(self, title, author_surname, year, metaonly):
        try:
            return json.dumps(
                self._controller.query_by_meta(title, author_surname, year, metaonly)
            )
        except:
            raise citedby_thrift.ServerError(
               'Server Error: icontroller.citedbymeta(%s, %s, %s, %s)'
               % (title, author_surname, year, metaonly)
            )

main = thriftpywrap.ConsoleApp(citedby_thrift.Citedby, Dispatcher)