#!/usr/bin/env python
# coding: utf-8

import os
import thriftpy

from thriftpy.rpc import make_client


# Examples using thrift
if __name__ == '__main__':

    citedby_thrift = thriftpy.load(os.path.join(os.path.dirname(
                                   os.path.abspath(__file__)), 'citedby.thrift'))

    client = make_client(citedby_thrift.Citedby, 'citedby.scielo.org', 11610)

    print(client.citedby_pid('S1516-89132010000300001', False))

    print(client.citedby_doi('10.1590/S1516-89132010000300001'))

    print(client.citedby_meta(title='Biochemical and morphological changes during the growth kinetics of Araucaria angustifolia suspension cultures'))
