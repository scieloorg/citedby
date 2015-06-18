# coding: utf-8

import requests
import logging

logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())


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


def load_from_crossref(doi):
    """
    Get the metadata from crossref
    """
    response = fetch_data('http://search.crossref.org/dois?q=%s' % doi).json()

    if len(response) == 0 or 'title' not in response[0]:
        return None

    return response[0]


def format_citation(citations):
    """
    Format the citation like:
        [{
            url: "http://www.scielo.cl/scielo.php?script=sci_arttext&pid=S0716-10182009000100012&lng=en&tlng=en",
            source: "Revista chilena de infectología",
            issn: "0716-1018",
            start_page: "105",
            end_page: "110",
            first_author: {
                surname: "ARAÚJO",
                given_names: "E. C."
            },
            code: "S0716-10182009000100012",
            title: "Fiebre tifoidea en Santiago, Chile y su control"
            authors: [
                {
                    surname: "ARAÚJO",
                    given_names: "E. C."
                }
            ],
        }]
    """
    l = []

    for citation in citations['hits']['hits']:
        l.append({
                'titles': citation['_source']['titles'],
                'url': citation['_source']['url'],
                'code': citation['_source']['code'],
                'source': citation['_source']['source'],
                'issn': citation['_source']['issn'],
                'authors': citation['_source']['authors'],
                'end_page': citation['_source']['end_page'],
                'start_page': citation['_source']['start_page'],
                'first_author': citation['_source']['first_author']})
    return l


def key_generator(namespace, fn, **kw):
    """
    Function to generate the keys of memcached.

    Truncate the key in 250 caracters
    """
    fname = fn.__name__

    def generate_key(*arg):

        key_str = namespace + fname + "_" + "_".join(unicode(s).encode(
                  'utf-8', 'ignore') for s in arg)

        return key_str[0:250]

    return generate_key
