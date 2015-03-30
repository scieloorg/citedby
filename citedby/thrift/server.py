#! /usr/bin/env python
#coding: utf-8

import os
import json
import thriftpy
from ConfigParser import SafeConfigParser

from thriftpy.thrift import TProcessor

from citedby.icitation import ICitation
from citedby.icontroller import (
                                query_by_pid,
                                query_by_doi,
                                query_by_meta
                                )

citedby_thrift = thriftpy.load(os.path.join(os.path.dirname(
                               os.path.abspath(__file__)), 'citedby.thrift'))


class Dispatcher(object):

    def __init__(self):

        #Get the config file at now, only production.ini

        config = SafeConfigParser()
        config.readfp(open('../../production.ini'))

        settings = dict(config.items('app:main'))

        self.index = ICitation(
            hosts=settings['elasticsearch_host'].split())


    def citedbypid(self, q, metaonly):

        try:
            return json.dumps(query_by_pid(self.index, q, metaonly))
        except:
            return citedby_thrift.ServerError(
                            'Server Error: icontroller.query_by_pid(%s, %s, %s)'
                             % (self.index, q, metaonly)).message


    def citedbydoi(self, q, metaonly):

        try:
            return json.dumps(query_by_doi(self.index, q, metaonly))
        except:
            return citedby_thrift.ServerError(
                            'Server Error: icontroller.query_by_doi(%s, %s, %s)'
                            % (self.index, q, metaonly)).message


    def citedbymeta(self, title, author_surname, year, metaonly):

        try:
            return json.dumps(
                query_by_meta(self.index, title, author_surname, year, metaonly))
        except:
            return citedby_thrift.ServerError(
                'Server Error: icontroller.citedbymeta(%s, %s, %s, %s, %s)'
                 % (self.index, title, author_surname, year, metaonly)).message


app = TProcessor(citedby_thrift.Citedby, Dispatcher())