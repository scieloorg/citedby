#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import os
import time
import gevent
import urllib2
import argparse
import itertools
import gevent.monkey
import thriftpy
from thriftpy.rpc import make_client


import articlemeta

# change to gevent.socket.socket
gevent.monkey.patch_socket()

THRIFT_SERVER = 'localhost'
THRIFT_PORT = 11610
THRIFT_FILE = os.path.join(os.path.dirname(
                           os.path.abspath(__file__)),
                           '../citedby/thrift/citedby.thrift')


class WarmCitedby(object):

    def __init__(self):

        citedby_thrift = thriftpy.load(THRIFT_FILE)

        self.client = make_client(citedby_thrift.Citedby,
                                  THRIFT_SERVER, THRIFT_PORT)

    def fetch(self, id):
        start = time.time()

        resp = self.client.citedby_pid(id, False)

        end = time.time()
        return id, len(resp), end-start

    def get_idents(self):
        """
        Get all ids.
        """
        ids = []

        for id in articlemeta.get_all_identifiers(onlyid=True):
            ids.append(id)

        return ids

    def run(self, itens=10, limit=10):

        offset = 0

        ids = self.get_idents()

        while True:

            _slice = itertools.islice(ids, offset, limit)
            lst_slice = list(_slice)

            print('From %d to %d' % (offset, limit))
            print('Slice: ' + str(lst_slice))

            if not lst_slice:
                break

            jobs = [gevent.spawn(self.fetch, id) for id in lst_slice]

            gevent.joinall(jobs, timeout=10)

            [print(job.value) for job in jobs]

            offset += itens
            limit += itens

            gevent.sleep(2)


def main():
    parser = argparse.ArgumentParser(
        description="Warm-up Citedby"
    )

    args = parser.parse_args()

    start = time.time()

    print('Warm-up Citedby cache from %s:%s' % (THRIFT_SERVER, THRIFT_PORT))

    WarmCitedby().run()

    end = time.time()

    print('Duration: %f' % (end-start))


if __name__ == '__main__':
    main()
