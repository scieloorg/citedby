#!/usr/bin/env python
#coding: utf-8

import os
import thriftpy


from thriftpy.rpc import make_client

citedby_thrift = thriftpy.load(os.path.join(os.path.dirname(
                               os.path.abspath(__file__)), 'citedby.thrift'))

client = make_client(citedby_thrift.Citedby, '127.0.0.1', 11610)


#Examples using thrift

print client.citedbypid('S1516-89132010000300001', False)

print client.citedbydoi('10.1590/S1516-89132010000300001')

print client.citedbymeta(title='Biochemical and morphological changes during the growth kinetics of Araucaria angustifolia suspension cultures')