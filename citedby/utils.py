# coding: utf-8

import requests


def load_from_crossref(doi):
    """
    Get the metadata from crossref
    """
    response = requests.get('http://search.crossref.org/dois?q=%s' % doi).json()

    if len(response) == 0:
        return None

    if not 'title' in response[0]:
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