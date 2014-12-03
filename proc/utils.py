#coding: utf-8

import requests
import logging

from xylose.scielodocument import Article

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

def diff_list(first_list, second_list):
    """
    Difference between two list

    :param first_list: First list for compare
    :param second_list: Second list for compare

    :returns: list of difference
    """
    return list(set(first_list) - set(second_list))

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

def citation_meta(art_meta_json):
    """
    This function receives a article meta JSON, transform it in an citation
    dicitionary, look the response example.

    :param art_meta_json: Article Meta JSON

    :returns:
            {
              "url": "scielo.php?script=sci_arttext&pid=S0101-31222002000100038",
              "source": "Revista Brasileira de Sementes",
              "issn": "0101-3122",
              "code": "S0101-31222002000100038",
              "collection": "scl",
              "titles": ["Adequação do ...", "Seconde title..."]
              "first_author": "Skapinakis P",
              "publication_year": "2013",
              "citations":
              [
                  {
                  "source": "Anais da Academia Brasileira de Ciências",
                  "first_author": "Moreira JK",
                  "title": "Germination of Croton ...",
                  "publication_year": "2004"
                  }
              ]
            }
    """
    art = Article(art_meta_json)

    c_dict = {}

    #List of titles
    c_dict['titles'] = []

    c_dict['url'] = art.html_url()
    c_dict['source'] = art.journal.title
    c_dict['issn'] = art.journal.scielo_issn
    c_dict['code'] = art.publisher_id

    if art.translated_titles():
        c_dict['titles'] = [t for l, t in art.translated_titles().items()]

    c_dict['titles'].append(art.original_title())
    c_dict['collection'] = art.collection_acronym
    c_dict['first_author'] = art.first_author
    c_dict['publication_year'] = art.publication_date[:4] if art.publication_date else ""

    if art.citations:

        art_citations = []

        for cit in art.citations:
            ac_dict = {}
            ac_dict['source'] = cit.source

            if cit.title():
                ac_dict['title'] = cit.title()
            elif cit.chapter_title:
                ac_dict['title'] = cit.chapter_title

            ac_dict['publication_year'] = cit.date[:4] if cit.date else ""

            ac_dict['first_author'] = cit.first_author

            art_citations.append(ac_dict)

        c_dict['citations'] = art_citations

    return c_dict
