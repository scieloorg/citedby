# coding: utf-8

from dogpile.cache import make_region
from pylibmc.test import make_test_client, NotAliveError

from icitation import ICitation
from utils import (load_from_crossref,
                   format_citation,
                   key_generator)

cache_region = make_region(name="citedby",
                           function_key_generator=key_generator)

cache_region.configure('dogpile.cache.bmemcached',
                       expiration_time=2592000,
                       arguments={'url': ['aquiles.scielo.org']})

# it`s must be on .ini file
es_hosts = ['esa.scielo.org:9200', 'esb.scielo.org:9200', 'esc.scielo.org:9200']

icindex = ICitation(hosts=es_hosts,
                    sniff_on_start=True,
                    sniff_on_connection_fail=True)


@cache_region.cache_on_arguments(namespace='CITEDBY_')
def query_by_pid(pid, metaonly=False):

    filters = {}
    src_fields = ['url', 'source', 'issn', 'collection', 'titles', 'code',
                  'first_author.surname', 'publication_year', 'authors',
                  'start_page', 'end_page', 'translated_titles', 'citations',
                  'doi']

    es_response = icindex.get_by_code(pid, _source_include=src_fields)

    if es_response['hits']['total'] == 0:
        return []

    article_meta = es_response['hits']['hits'][0]['_source']

    citations = []
    
    article_meta['total_received'] = 0
    article_meta['total_granted'] = 0
    
    if ('titles' in article_meta and 'first_author' in article_meta and 'publication_year' in article_meta):

        filters['titles'] = article_meta['titles']
        filters['author_surname'] = article_meta['first_author']['surname']
        filters['year'] = article_meta['publication_year']

        meta = icindex.search_citation(**filters)

        if meta:
            citations = format_citation(meta)
            article_meta['total_received'] = len(citations)

    if 'citations' in article_meta:
        article_meta['total_granted'] = len(article_meta['citations'])
        del(article_meta['citations'])

    if metaonly:
        return {'article': article_meta}
    else:
        return {'article': article_meta, 'cited_by': citations}


@cache_region.cache_on_arguments(namespace='CITEDBY_')
def query_by_doi(doi, metaonly=False):

    meta = load_from_crossref(doi)

    if not meta:
        return []

    article_meta = {}
    article_meta['title'] = [meta['title']]
    article_meta['author'] = ''
    article_meta['year'] = meta['year']

    citations = format_citation(icindex.search_citation(
                    titles=[article_meta['title']], year=article_meta['year']))

    article_meta['total_cited_by'] = len(citations)

    if metaonly:
        return {'article': article_meta}
    else:
        return {'article': article_meta, 'cited_by': citations}


@cache_region.cache_on_arguments(namespace='CITEDBY_')
def query_by_meta(title='', author_surname='', year='', metaonly=False):

    article_meta = {}
    article_meta['title'] = title
    article_meta['author'] = author_surname
    article_meta['year'] = year

    citations = format_citation(icindex.search_citation(
                    titles=[title], author_surname=author_surname, year=year))

    article_meta['total_cited_by'] = len(citations)

    if metaonly:
        return {'article': article_meta}
    else:
        return {'article': article_meta, 'cited_by': citations}


def get_status_memcached(mems_addr=None):
    '''
    Get the status of caches.

    :param mems_addr: list of memcached address IP:PORT.
    '''
    memcacheds = {}

    for mem in mems_addr:

        addr, port = mem.split(':')

        try:
            alive = bool(make_test_client(host=addr, port=port))
            memcacheds[mem] = alive
        except NotAliveError:
            memcacheds[mem] = False

    return memcacheds


def get_status_cluster():
    '''
    Get the status of cluster.
    '''
    return icindex._ping()
