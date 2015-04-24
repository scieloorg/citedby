#! /usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os
import json
import argparse
import thriftpy
from thriftpy.rpc import make_server

from citedby.icontroller import (query_by_pid,
                                 query_by_doi,
                                 query_by_meta)

ADDRESS = '0.0.0.0'
PORT = '11610'

citedby_thrift = thriftpy.load(os.path.join(os.path.dirname(
                               os.path.abspath(__file__)), 'citedby.thrift'))


class Dispatcher(object):

    def citedby_pid(self, q, metaonly):

        try:
            return json.dumps(query_by_pid(q, metaonly))
        except:
            return citedby_thrift.ServerError(
                            'Server Error: icontroller.query_by_pid(%s, %s, %s)'
                            % (q, metaonly)).message

    def citedby_doi(self, q, metaonly):
        try:
            return json.dumps(query_by_doi(q, metaonly))
        except:
            return citedby_thrift.ServerError(
                            'Server Error: icontroller.query_by_doi(%s, %s, %s)'
                            % (q, metaonly)).message

    def citedby_meta(self, title, author_surname, year, metaonly):

            try:
                return json.dumps(
                    query_by_meta(title, author_surname, year, metaonly))
            except:
                return citedby_thrift.ServerError(
                       'Server Error: icontroller.citedbymeta(%s, %s, %s, %s, %s)'
                       % (title, author_surname, year, metaonly)).message


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

    args = parser.parse_args()

    server = make_server(citedby_thrift.Citedby,
                         Dispatcher(), args.address, args.port)

    print("Started server on IP: %s:%s" % (args.address, args.port))

    server.serve()


if __name__ == "__main__":
    main()
