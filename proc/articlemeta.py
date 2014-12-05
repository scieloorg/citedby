#coding: utf-8

import requests
import logging

logger = logging.getLogger(__name__)

logger.addHandler(logging.NullHandler())

URL = 'http://articlemeta.scielo.org'
IDENT_ENDPOINT = '/api/v1/article/identifiers'
ARTICLE_ENDPOINT = '/api/v1/article'

def fetch_data(resource):
    """
    Fetches any resource.

    :param resource: any resource
    :returns: requests.response object

    The param resource must be a valid URL
    example: ``/api/v1/article?code=S2238-10312012000300006``
    """
    try:
        response = requests.get(resource)
    except requests.exceptions.RequestException as e:
        logger.error('%s. Unable to connect to resource.' % e)
    else:
        logger.debug('Get resource: %s' % resource)
        return response

def get_identifiers_count(endpoint=None):
    """
    Get total of identifiers in Article Meta API.

    :param endpoint: the endpoint of identifiers in Article Meta.

    Endpoint: ``/api/v1/article/identifiers``

    :returns: integer
    """

    if not endpoint:
        endpoint = URL + IDENT_ENDPOINT

    return int(fetch_data(endpoint).json()['meta']['total'])

def get_all_identifiers(offset_range=1000):
    """
    Get all identifiers by Article Meta API

    :param offset_range: paging through API result, default:1000.

    Endpoint: ``api/v1/article/identifiers?offset=1000``

    :returns: return a generator with a tuple ``(collection, PID)``,
    ex.: mexS0036-36342014000100009
    """

    offset = 0

    logger.debug('Get all identifiers from Article Meta, please wait... this while take while!')

    while True:

        resp = fetch_data(URL + IDENT_ENDPOINT + '?offset=%d' % offset).json()

        for identifier in resp['objects']:
            logger.debug('Get article with code: %s from: %s' %
                (identifier['code'], identifier['collection']))
            yield (identifier['collection'], identifier['code'])

        offset += offset_range

        if offset > resp['meta']['total']:
            raise StopIteration

def get_article(collection, code):
    """
    Get article meta data by code

    :param code: SciELO PID(Publisher Identifier)
    :param collection: collection acronym

    Endpoint: ``/api/v1/pid/?q=S0101-31222002000100038``

    :returns: Article JSON
    """
    logger.debug('Get article with code: %s by collection %s' % (code, collection))

    return fetch_data(URL + ARTICLE_ENDPOINT +
        '?code=%s&collection=%s' % (code, collection)).json()
