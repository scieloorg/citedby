# coding: utf-8

import requests
import logging

logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())

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


def key_generator(namespace, fn, **kw):
    """
    Function to generate the keys of memcached.

    Truncate the key in 250 caracters
    """
    fname = fn.__name__

    def generate_key(*arg):

        key_str = namespace + fname + "_" + "_".join(str(s).encode('ascii', 'ignore') for s in arg)

        return key_str[0:250]

    return generate_key


def fetch_data(resource):
    """
    Fetches any resource.

    :param resource: any resource
    :returns: requests.response object

    The param resource must be a valid URL
    example: ``http:///api/v1/article?code=S2238-10312012000300006``
    """
    try:
        response = requests.get(resource)
    except requests.exceptions.RequestException as e:
        logger.error('%s. Unable to connect to resource.' % e)
    else:
        logger.debug('Get resource: %s' % resource)
        return response
