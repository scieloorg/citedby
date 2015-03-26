#!/usr/bin/env python
#coding: utf-8

import thriftpy

from thriftpy.rpc import make_client

citedby_thrift = thriftpy.load("citedby.thrift")

client = make_client(citedby_thrift.Citedby, '127.0.0.1', 11610)

print client.citedbypid('param_test1', 'param_test2')