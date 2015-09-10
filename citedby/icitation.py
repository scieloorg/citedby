# coding: utf-8
from elasticsearch import Elasticsearch
from elasticsearch import helpers


class ICitation(object):

    def __init__(self, hosts=None, index="citations", **kwargs):
        """
        On class initialization is created a connection to ES and
        verify if is up with citation index, raise except otherwise.

        :param hosts: list of nodes we should connect
        :param kwargs: elasticsearch params, see:
        http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch.Elasticsearch
        """
        self.index = index
        self.es_conn = Elasticsearch(hosts, **kwargs)

        if kwargs.get('check_es', None):
            if not self._ping():
                raise Exception("The Elasticsearch is down!")

        if kwargs.get('check_index', None):
            # Verify if index exists
            if not self._exists():
                raise Exception("The index doesnt exist!")

    def _ping(self):
        """
        :returns: Boolean ``True`` if ES is up, ``False`` otherwise
        """
        return bool(self.es_conn.ping())

    def _exists(self):
        """
        Verify if the citation index exists.

        :returns: Boolean ``True`` if exists or ``False`` otherwise.
        """
        return bool(self.es_conn.indices.exists(index=self.index))

    def count_citation(self):
        """
        Count the total of citation in citation index.

        :returns: Interger.
        """
        return int(self.es_conn.count(index=self.index)['count'])

    def get_by_code(self, code, **kwargs):
        """
        Get article by code
        """
        return self.es_conn.search(index=self.index,
                                   body={
                                      "query": {"match_phrase": {
                                        "code": code
                                      }}
                                    }, **kwargs)

    def get_all(self, query=None, size=1000):
        """
        Get all using query from the SciELO citation index.

        :param size: Number of hits to return (default: 1000).
        :param query(DSL): get by param DSL query or it will use DSL match_all
        query

        :returns: A generator with citation data structure.
        """
        from_ = 0

        if not query:
            query = {"query": {"match_all": {}, "fields": []}}

        while True:

            resp = self.es_conn.search(index=self.index, from_=from_,
                                       size=size, body=query)

            for citation in resp['hits']['hits']:
                yield citation

            from_ += size

            if from_ > resp['hits']['total']:
                raise StopIteration

    def get_identifiers(self):
        """
        Get all identifiers in index citation. This method configure the query
        to not get any field just identifiers and increase the size param.

        :returns: a list content tuple, like: ('acronym of collection', SciELO PID).
        """
        all_citations = self.get_all(query={"query": {"match_all": {}},
                                            "_source": ["collection", "code"]},
                                     size=10000)

        return [(i['_source']['collection'], i['_source']['code'])
                for i in all_citations]

    def index_citation(self, doc, article_id):
        """
        Index article and validate if have some attributes.

        :param doc: a dictionary that must have two keys ``code`` and
        ``collection``, must be a dicionary.

        :returns:{
                  "_index":"citations",
                  "_type":"citation",
                  "_id":"S0120-53072010000300001-scl"
                  "_version":1,
                  "created":true
                 } (Elasticsearch response)
        """

        if not isinstance(doc, dict):
            raise TypeError('param doc must be a dicionary!')

        if not ('code' or 'collection') in doc:
            raise ValueError('param doc must contain keys code and collection')

        return self.es_conn.index(index=self.index, id=article_id, doc_type='citation',
                                  body=doc)

    def bulk_citation(self, articles):
        """
        Index article and validate if have some attributes.

        :param articles: list of articles

        """

        return helpers.bulk(self.es_conn, articles)

    def del_all_citation(self):
        """
        Delete all documents from index citations, try to delete index only if
        it exists in Elasticsearch.

        This method can returns a Elasticsearch response or None if the index
        doesnt exists.

        :returns:{
                 "_indices":
                    {"citations":
                        {"_shards":
                            {"successful": 5, "failed": 0, "total": 5}
                        }
                    }
                }
        """

        if self._exists():
            return self.es_conn.delete_by_query(index=self.index,
                                                body={"query": {"match_all": {}}})

    def del_citation(self, ident):
        """
        Remove citation by identifier, (u'S0898-9081938912378', u'scl').

        :returns:{
                 "_indices":
                    {"citations":
                        {"_shards":
                            {"successful": 5, "failed": 0, "total": 5}
                        }
                    }
                }
        """

        if self._exists():
            return self.es_conn.delete_by_query(index=self.index,
                                                body={
                                                      "query": {
                                                        "bool": {
                                                          "must": [
                                                            {"match_phrase": {"code": ident[1]}},
                                                            {"match_phrase": {"collection": ident[0]}}
                                                          ]
                                                        }
                                                      }
                                                    })

    def search_citation(self, titles, author_surname=None, year=None, size=1000):
        """
        Search citations by ``title``, ``author`` and ``year``.

        :param titles: Titles of article in any language
        :param author_surname: The surname of first author
        :param year: Is the publication year

        This method will search for citations that have smilarity titles and
        exact first author surname and exact publication_year
        """

        should_param = []
        must_param = []

        if not titles or not isinstance(titles, list):
            None

        for title in titles:
            should_param.append({
                            "fuzzy_like_this_field": {
                                "citations.title": {
                                    "like_text": title,
                                    "max_query_terms": 10,
                                    "prefix_length": 3
                                }
                            }
                        })

        if author_surname:
            must_param.append({
                        "match": {
                          "citations.first_author.surname": author_surname
                            }
                        })

        if year:
            must_param.append({
                          "match": {
                            "citations.publication_year": year
                          }
                        })

        return self.es_conn.search(index=self.index,
                                   body={
                                      "query":
                                      {
                                        "nested": {
                                          "path": "citations",
                                          "query": {
                                              "bool": {
                                                "must": must_param,
                                                "should": should_param,
                                                "minimum_number_should_match": 1
                                              }
                                          }
                                        }
                                      }
                                    }, size=size)
