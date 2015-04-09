#!/usr/bin/python
#coding: utf-8

from __future__ import print_function

import time
import gevent
import urllib2
import argparse
import itertools
import gevent.monkey

import articlemeta

#change to gevent.socket.socket
gevent.monkey.patch_socket()


class WarmCitedby(object):

    def __init__(self, url):
        self.url = url

    def fetch(self, id):
        start = time.time()
        resp = urllib2.urlopen(self.url + 'api/v1/pid/?q=%s' % id).read()
        end = time.time()
        return id, len(resp), end-start

    def run(self, itens=10, limit=10):
        print('Warm-up Citedby cache from url %s' % self.url)

        offset = 0
        limit = limit
        itens = itens

        ids = articlemeta.get_all_identifiers(limit=10000, offset_range=10000,
                                              onlyid=True)

        while True:

            id_slice = itertools.islice(ids, offset, limit)

            print('From %d to %d' % (offset, limit))

            if not id_slice:
                break

            jobs = [gevent.spawn(self.fetch, id) for id in id_slice]

            gevent.joinall(jobs)

            [print(job.value) for job in jobs]

            offset += itens
            limit += itens

            gevent.sleep(0)


def main():
    parser = argparse.ArgumentParser(
        description="Warm-up Citedby Web."
    )

    parser.add_argument(
        '--url',
        '-u',
        default='http://citedby.scielo.org/',
        help='URL of Citedby, default: http://citedby.scielo.org/'
    )

    args = parser.parse_args()

    start = time.time()
    WarmCitedby(args.url).run(itens=20, limit=20)
    end = time.time()

    print('Ducration: %d' (end-start))


if __name__ == '__main__':
    main()