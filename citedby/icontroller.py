# coding: utf-8
import urllib2
import json

def load_document_meta_from_crossref(doi):
    response = json.loads(urllib2.urlopen('http://search.crossref.org/dois?q=%s' % doi).read())

    if not len(response) > 0:
        return None

    if not 'title' in response[0]:
        return None

    if not response[0]['title']:
        return None

    return response[0]


def format_citation(citations):
    """
    Format the citation like:
        [{
            url: "http://www.scielo.cl/scielo.php?script=sci_arttext&pid=S0716-10182009000100012&lng=en&tlng=en",
            source: "Revista chilena de infectología",
            issn: "0716-1018",
            code: "S0716-10182009000100012",
            title: "Fiebre tifoidea en Santiago, Chile y su control"
        }]
    """
    l = []

    for citation in citations['hits']['hits']:
        l.append({
                'titles': citation['_source']['titles'],
                'url': citation['_source']['url'],
                'code': citation['_source']['code'],
                'source': citation['_source']['source'],
                'issn': citation['_source']['issn']})
    return l


def query_by_pid(index, pid):

    filters = {}
    src_fields = ['url', 'source', 'issn', 'collection', 'titles', 'code', 'first_author.surname', 'publication_year']

    #precisa evitar o index exception
    article = index.get_by_code(pid, _source_include=src_fields)['hits']['hits'][0]['_source']

    if ('titles' in article and 'first_author' in article and 'publication_year' in article):

        filters['titles'] = article['titles']
        filters['author_surname'] = article['first_author']['surname']
        filters['year'] = article['publication_year']

        citations = format_citation(index.search_citation(**filters))
        
    else:
        citations = []

    return {'article': article, 'citedby':citations}


def query_by_doi(index, doi):
    article_meta = load_document_meta_from_crossref(doi)

    if not article_meta:
        return None

    citations = format_citation(index.search_citation(titles=[article_meta['title']], year=article_meta['year']))

    return {'article': article_meta, 'cited_by': citations}


def query_by_meta(index, title='', author_surname='', year=''):

    if not title:
        return None

    article_meta = {}
    article_meta['title'] = title
    article_meta['author'] = author_surname
    article_meta['year'] = year

    citations = format_citation(index.search_citation(titles=[title], author_surname=author_surname, year=year))

    return {'article': article_meta, 'cited_by': citations}
