#! /usr/bin/env python
#coding: utf-8

import thriftpy

from thriftpy.thrift import TProcessor


class Dispatcher(object):

    def citedbypid(self, q, metaonly):
        return "citedbypid"

    def citedbydoi(self, q, metaonly):
        return "citedbydoi"

    def citedbymeta(self, title, author_surname, year, metaonly):
        return "citedbymeta"


citedby_thrift = thriftpy.load('citedby.thrift')

app = TProcessor(citedby_thrift.Citedby, Dispatcher())