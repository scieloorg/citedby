# coding: utf-8
import logging
from dogpile.cache import make_region
from pylibmc.test import make_test_client, NotAliveError

import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from thrift_clients import clients
from utils import load_from_crossref, format_citation
import utils


cache_region = make_region(
    name="citedby",
    function_key_generator=utils.dogpile_controller_key_generator
)


class ServerError(Exception):

    def __init__(self, value):
        self.message = 'Server Error: %s' % str(value)

    def __str__(self):
        return repr(self.message)


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


def articlemeta(host='articlemeta.scielo.org:11720'):

    address, port = host.split(':')

    return clients.ArticleMeta(address, port)


def controller(*args, **kwargs):

    return Controller(*args, **kwargs)


class Controller(Elasticsearch):

    articlemeta_client = articlemeta()
    base_index = 'citations'

    def _query_dispatcher(self, *args, **kwargs):

        kwargs['index'] = self.base_index

        try:
            data = self.search(*args, **kwargs)
        except elasticsearch.SerializationError:
            message = 'ElasticSearch SerializationError'
            logging.error(message)
            raise ServerError(message)
        except elasticsearch.TransportError as e:
            message = 'ElasticSearch TransportError: %s' % e.error
            logging.error(message)
            raise ServerError(message)
        except elasticsearch.ConnectionError as e:
            message = 'ElasticSearch ConnectionError: %s' % e.error
            logging.error(message)
            raise ServerError(message)
        except:
            message = "Unexpected error: %s" % sys.exc_info()[0]
            logging.error()
            raise ServerError(message)

        return data

    def bibliometric_search(self, parameters):

        query_result = self._query_dispatcher(**parameters)

        return query_result

    def load_mapping(self):

        citations_settings_mappings = {
            "mappings": {
                "citation": {
                    "dynamic": "strict",
                    "properties": {
                        "authors": {
                            "dynamic": "strict",
                            "properties": {
                                "given_names": {
                                    "type": "string"
                                },
                                "role": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "surname": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "xref": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                }
                            }
                        },
                        "code": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "pid": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "collection": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "subject_areas": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "document_type": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "doi": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "end_page": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "first_author": {
                            "dynamic": "strict",
                            "properties": {
                                "given_names": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "role": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "surname": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "xref": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                }
                            }
                        },
                        "issn": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "publication_year": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "source": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "start_page": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "titles": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "url": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_authors": {
                            "dynamic": "strict",
                            "properties": {
                                "given_names": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                },
                                "surname": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                }
                            }
                        },
                        "reference_end_page": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_first_author": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_first_author_cleaned": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_publication_year": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_source": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_source_cleaned": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_start_page": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_title": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_title_cleaned": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_volume": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_number": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "reference_index_number": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                }
            }
        }

        self.indices.create(
            index=self.base_index, body=citations_settings_mappings, ignore=400)

    def _ping(self):
        """
        :returns: Boolean ``True`` if ES is up, ``False`` otherwise
        """
        return bool(self.ping())

    def index_reset(self):
        self.indices.delete(index=self.base_index, ignore=[400, 404])
        self.load_mapping()

    def index_citation(self, doc, article_id):
        """
        Index article and validate if have some attributes.

        :param doc: a dictionary that must have two keys ``code`` and
        ``collection``, must be a dicionary.
        """

        if not isinstance(doc, dict):
            raise TypeError('param doc must be a dicionary!')

        if not ('code' or 'collection') in doc:
            raise ValueError('param doc must contain keys code and collection')

        return self.index(index=self.base_index, id=article_id, doc_type='citation', body=doc)

    def del_citation(self, collection, code):

        body = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"code": code}},
                        {"match": {"collection": collection}}
                    ]
                }
            },
            "size": 10000
        }

        itens = self.search(index=self.base_index, body=body)

        for item in itens.get('hits', {'hits': []})['hits']:
            ident = item.get('_id', None)
            if not ident:
                continue
            self.delete(index=self.base_index, doc_type='citation', id=ident)

    def search_citation(self, titles, author_surname=None, year=None, size=1000):
        """
        Search citations by ``title``, ``author`` and ``year``.

        :param titles: Titles of article in any language
        :param author_surname: The surname of first author
        :param year: Is the publication year

        This method will search for citations that have similar titles and
        exact first author surname and exact publication_year
        """

        must_param = []

        if not titles or not isinstance(titles, list):
            return None

        titles = [utils.cleanup_string(i) for i in titles if i]

        if len(titles) == 0:
            return None

        for title in titles:
            must_param.append({
                "fuzzy": {
                    "reference_title_cleaned": {
                        "value": title,
                        "fuzziness": 2
                    }
                }
            })

        if author_surname:
            must_param.append({
                "fuzzy": {
                    "reference_first_author_cleaned": {
                        "value": utils.cleanup_string(author_surname),
                        "fuzziness": 2
                    }
                }
            })

        if year:
            must_param.append({
                "match": {
                    "reference_publication_year": year
                }
            })

        body = {
            "query": {
                "bool": {
                    "must": must_param,
                    "minimum_number_should_match": 1
                }
            }
        }

        return self._query_dispatcher(body=body, size=size)

    @cache_region.cache_on_arguments()
    def query_by_pid(self, pid, collection=None, metaonly=False):

        filters = {}

        document = self.articlemeta_client.document(pid, collection=collection)

        if not document:
            return []

        article_meta = {}
        article_meta['code'] = document.publisher_id
        article_meta['start_page'] = document.start_page
        article_meta['end_page'] = document.end_page
        article_meta['first_author'] = document.authors[0] if document.authors and len(document.authors) > 0 else None
        article_meta['issn'] = document.journal.scielo_issn
        article_meta['publication_year'] = document.publication_date[0:4]
        article_meta['url'] = document.html_url()
        article_meta['collection'] = document.collection_acronym
        article_meta['authors'] = document.authors
        article_meta['translated_titles'] = document.translated_titles()
        article_meta['doi'] = document.doi

        article_meta['titles'] = []

        if document.original_title():
            article_meta['titles'].append(document.original_title())

        if document.translated_titles():
            article_meta['titles'] + [t for l, t in document.translated_titles().items() if t]

        citations = []

        article_meta['total_received'] = 0

        if (article_meta.get('titles', False) and article_meta.get('first_author', False) and article_meta.get('publication_year', False)):

            filters['titles'] = article_meta.get('titles', None)
            filters['author_surname'] = article_meta.get('first_author', {}).get('surname', None)
            filters['year'] = article_meta.get('publication_year', None)

            meta = self.search_citation(**filters)

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

    @cache_region.cache_on_arguments()
    def query_by_doi(self, doi, metaonly=False):

        meta = load_from_crossref(doi)

        if not meta:
            return []

        article_meta = {}
        article_meta['title'] = [meta['title']]
        article_meta['author'] = ''
        article_meta['year'] = meta['year']

        meta = self.search_citation(titles=[article_meta['title']], year=article_meta['year'])

        if meta:
            citations = format_citation(meta)

        article_meta['total_received'] = len(citations)

        if metaonly:
            return {'article': article_meta}
        else:
            return {'article': article_meta, 'cited_by': citations}

    @cache_region.cache_on_arguments()
    def query_by_meta(self, title='', author_surname='', year='', metaonly=False):

        article_meta = {}
        article_meta['title'] = title
        article_meta['author'] = author_surname
        article_meta['year'] = year

        meta = self.search_citation(titles=[title], author_surname=author_surname, year=year)

        if meta:
            citations = format_citation(meta)

        article_meta['total_received'] = len(citations)

        if metaonly:
            return {'article': article_meta}
        else:
            return {'article': article_meta, 'cited_by': citations}

    def get_status_cluster(self):
        '''
        Get the status of cluster.
        '''
        return self._ping()
