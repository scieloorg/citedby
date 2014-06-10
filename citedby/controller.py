# coding: utf-8

import utils
import unicodedata
import string
import urllib2
import json

from xylose.scielodocument import Article


def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if unicodedata.category(x)[0] == 'L').lower()


def preparing_key(title='', author='', year=''):

    if not title:
        return None

    title_key = title
    title_key += author

    return remove_accents(title_key)+year


def load_article_title_keys(article):
    titles = []

    data = {}
    data['year'] = article.publication_date[0:4]
    data['author'] = article.authors[0]['given_names']+article.authors[0]['surname']

    if article.original_title():
        data['title'] = article.original_title()
        titles.append(preparing_key(article.original_title()))
        titles.append(preparing_key(**data))

    if article.translated_titles():
        for title in article.translated_titles().values():
            data['title'] = title
            titles.append(preparing_key(title))
            titles.append(preparing_key(**data))

    return titles


def load_article(coll, pid):
    query = coll.find_one({'code': pid}, {'article': 1, 'title': 1})

    if not query:
        return None

    return Article(query)


def load_document_meta(article):

    article_meta = {
        'code': article.publisher_id,
        'title': article.original_title(),
        'issn': article.any_issn(),
        'source': article.journal_title,
        'url': article.html_url
    }

    return article_meta


def query_by_pid(coll, pid):
    article = load_article(coll, pid)

    if not article:
        return None

    title_keys = load_article_title_keys(article)
    query = coll.find({'citations_keys': {'$in': title_keys}}, {'article': 1, 'title': 1})

    citations = None
    if query:
        citations = []
        for doc in query:
            citation = Article(doc)
            meta = load_document_meta(citation)
            citations.append(meta)

    article_meta = load_document_meta(article)

    return {'article': article_meta, 'cited_by': citations}


def load_document_meta_from_crossref(doi):
    response = json.loads(urllib2.urlopen('http://search.crossref.org/dois?q=%s' % doi).read())

    if not len(response) > 0:
        return None

    if not 'title' in response[0]:
        return None

    if not response[0]['title']:
        return None

    return response[0]


def query_by_doi(coll, doi):
    article_meta = load_document_meta_from_crossref(doi)

    if not article_meta:
        return None

    title_key = preparing_key(title=article_meta['title'])

    query = coll.find({'citations_keys': title_key}, {'article': 1, 'title': 1})

    citations = None
    if query:
        citations = []
        for doc in query:
            citation = Article(doc)
            meta = load_document_meta(citation)
            citations.append(meta)

    return {'article': article_meta, 'cited_by': citations}


def query_by_meta(coll, title='', author='', year=''):

    article_meta = {}
    article_meta['title'] = title
    article_meta['author'] = author
    article_meta['year'] = year

    title_key = preparing_key(title, author, year)

    if not title_key:
        return None

    query = coll.find({'citations_keys': title_key}, {'article': 1, 'title': 1})

    citations = None
    if query:
        citations = []
        for doc in query:
            citation = Article(doc)
            meta = load_document_meta(citation)
            citations.append(meta)

    return {'article': article_meta, 'cited_by': citations}
