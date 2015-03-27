# coding: utf-8
from utils import (
                   load_from_crossref,
                   format_citation
                   )


def query_by_pid(index, pid, metaonly=False):

    filters = {}
    src_fields = ['url', 'source', 'issn', 'collection', 'titles', 'code', 'first_author.surname', 'publication_year']

    es_response = index.get_by_code(pid, _source_include=src_fields)

    if es_response['hits']['total'] == 0:
        return []

    article_meta = es_response['hits']['hits'][0]['_source']

    citations = []

    if ('titles' in article_meta and 'first_author' in article_meta and 'publication_year' in article_meta):

        filters['titles'] = article_meta['titles']
        filters['author_surname'] = article_meta['first_author']['surname']
        filters['year'] = article_meta['publication_year']

        citations = format_citation(index.search_citation(**filters))

    article_meta['total_cited_by'] = len(citations)

    if metaonly:
        return {'article': article_meta}
    else:
        return {'article': article_meta, 'cited_by':citations}


def query_by_doi(index, doi, metaonly=False):
    meta = load_from_crossref(doi)

    if not meta:
        return []

    article_meta = {}
    article_meta['title'] = [meta['title']]
    article_meta['author'] = ''
    article_meta['year'] = meta['year']

    citations = format_citation(index.search_citation(titles=[article_meta['title']], year=article_meta['year']))

    article_meta['total_cited_by'] = len(citations)

    if metaonly:
        return {'article': article_meta}
    else:
        return {'article': article_meta, 'cited_by':citations}


def query_by_meta(index, title='', author_surname='', year='', metaonly=False):

    article_meta = {}
    article_meta['title'] = title
    article_meta['author'] = author_surname
    article_meta['year'] = year

    citations = format_citation(index.search_citation(titles=[title], author_surname=author_surname, year=year))

    article_meta['total_cited_by'] = len(citations)

    if metaonly:
        return {'article': article_meta}
    else:
        return {'article': article_meta, 'cited_by':citations}
