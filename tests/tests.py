# coding: utf-8

import unittest
import ConfigParser
import urllib2
import json

from mocker import ANY, MockerTestCase
from xylose.scielodocument import Article

from citedby import utils
from citedby import controller
from . import fixtures


class ControllerTests(MockerTestCase):

    def test_preparing_key_title(self):

        title = u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog'

        result = controller.preparing_key(title=title)

        expected = u'powerspectralanalysisofheartrateandarterialpressurevariabilitiesasamarkerofsympathovagalinteractioninmanandconsciousdog'

        self.assertEqual(result, expected)

    def test_preparing_key_title_author(self):

        title = u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog'
        author = u'M. Pagani'

        result = controller.preparing_key(title=title, author=author)

        expected = u'powerspectralanalysisofheartrateandarterialpressurevariabilitiesasamarkerofsympathovagalinteractioninmanandconsciousdogmpagani'

        self.assertEqual(result, expected)


    def test_preparing_key_title_author_year(self):

        title = u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog'
        author = u'M. Pagani'
        year = u'1986'

        result = controller.preparing_key(title=title, author=author, year=year)

        expected = u'powerspectralanalysisofheartrateandarterialpressurevariabilitiesasamarkerofsympathovagalinteractioninmanandconsciousdogmpagani1986'

        self.assertEqual(result, expected)

    def test_preparing_key_title_year(self):

        title = u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog'
        year = u'1986'

        result = controller.preparing_key(title=title, year=year)

        expected = u'powerspectralanalysisofheartrateandarterialpressurevariabilitiesasamarkerofsympathovagalinteractioninmanandconsciousdog1986'

        self.assertEqual(result, expected)

    def test_query_by_meta(self):
        mock_coll = self.mocker.mock()
        mock_coll.find(ANY, ANY)
        self.mocker.result(fixtures.articles)
        self.mocker.replay()

        result = controller.query_by_meta(mock_coll, 
            title=u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog',
            author=u'M. Pagani',
            year=u'1986')

        expected = { 
                'article':{
                    "title": u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog',
                    "author": u'M. Pagani',
                    "year": u"1986"
                },
                'cited_by':[{
                        'code': u'S0104-07072013000100023',
                        'title': u'title en',
                        'issn': u'0104-0707',
                        'source': u'Texto & Contexto - Enfermagem',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-07072013000100023'
                    },{
                        'code': u'S1414-81452012000300003',
                        'title': u'title pt',
                        'issn': u'1414-8145',
                        'source': u'Escola Anna Nery',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1414-81452012000300003'
                    }
                ]
            }

        self.assertEqual(result, expected)

    def test_query_by_meta_no_author(self):
        mock_coll = self.mocker.mock()
        mock_coll.find(ANY, ANY)
        self.mocker.result(fixtures.articles)
        self.mocker.replay()

        result = controller.query_by_meta(mock_coll, 
            title=u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog',
            year=u'1986')

        expected = { 
                'article':{
                    'title': u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog',
                    'author': '',
                    'year': u'1986'
                },
                'cited_by':[{
                        'code': u'S0104-07072013000100023',
                        'title': u'title en',
                        'issn': u'0104-0707',
                        'source': u'Texto & Contexto - Enfermagem',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-07072013000100023'
                    },{
                        'code': u'S1414-81452012000300003',
                        'title': u'title pt',
                        'issn': u'1414-8145',
                        'source': u'Escola Anna Nery',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1414-81452012000300003'
                    }
                ]
            }

        self.assertEqual(result, expected)

    def test_query_by_meta_just_title(self):
        mock_coll = self.mocker.mock()
        mock_coll.find(ANY, ANY)
        self.mocker.result(fixtures.articles)
        self.mocker.replay()

        result = controller.query_by_meta(mock_coll, 
            title=u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog')

        expected = { 
                'article':{
                    'title': u'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog',
                    'author': '',
                    'year': u''
                },
                'cited_by':[{
                        'code': u'S0104-07072013000100023',
                        'title': u'title en',
                        'issn': u'0104-0707',
                        'source': u'Texto & Contexto - Enfermagem',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-07072013000100023'
                    },{
                        'code': u'S1414-81452012000300003',
                        'title': u'title pt',
                        'issn': u'1414-8145',
                        'source': u'Escola Anna Nery',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1414-81452012000300003'
                    }
                ]
            }

        self.assertEqual(result, expected)

    def test_query_by_meta_no_title(self):
        mock_coll = self.mocker.mock()
        self.mocker.replay()

        result = controller.query_by_meta(mock_coll, 
            author=u'M. Pagani',
            year=u'1986')

        self.assertEqual(result, None)

    def test_query_by_doi(self):
        load_document_meta_from_crossref = self.mocker.replace(controller.load_document_meta_from_crossref)
        load_document_meta_from_crossref(ANY)
        self.mocker.result(fixtures.doi_response[0])

        mock_coll = self.mocker.mock()
        mock_coll.find(ANY, ANY)
        self.mocker.result(fixtures.articles)
        self.mocker.replay()

        expected = { 
                'article':{
                    "normalizedScore": 100,
                    "doi": u"http://dx.doi.org/10.1161/01.res.59.2.178",
                    "title": u"Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog",
                    "coins": u"ctx_ver=Z39.88-2004&amp;rft_id=info%3Adoi%2Fhttp%3A%2F%2Fdx.doi.org%2F10.1161%2F01.res.59.2.178&amp;rfr_id=info%3Asid%2Fcrossref.org%3Asearch&amp;rft.atitle=Power+spectral+analysis+of+heart+rate+and+arterial+pressure+variabilities+as+a+marker+of+sympatho-vagal+interaction+in+man+and+conscious+dog&amp;rft.jtitle=Circulation+Research&amp;rft.date=1986&amp;rft.volume=59&amp;rft.issue=2&amp;rft.spage=178&amp;rft.epage=193&amp;rft.aufirst=M.&amp;rft.aulast=Pagani&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.au=M.+Pagani&amp;rft.au=+F.+Lombardi&amp;rft.au=+S.+Guzzetti&amp;rft.au=+O.+Rimoldi&amp;rft.au=+R.+Furlan&amp;rft.au=+P.+Pizzinelli&amp;rft.au=+G.+Sandrone&amp;rft.au=+G.+Malfatto&amp;rft.au=+S.+Dell%27Orto&amp;rft.au=+E.+Piccaluga",
                    "fullCitation": u"M. Pagani, F. Lombardi, S. Guzzetti, O. Rimoldi, R. Furlan, P. Pizzinelli, G. Sandrone, G. Malfatto, S. Dell'Orto, E. Piccaluga, 1986, 'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog', <i>Circulation Research</i>, vol. 59, no. 2, pp. 178-193",
                    "score": 18.42057,
                    "year": u"1986"
                },
                'cited_by':[{
                        'code': u'S0104-07072013000100023',
                        'title': u'title en',
                        'issn': u'0104-0707',
                        'source': u'Texto & Contexto - Enfermagem',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-07072013000100023'
                    },{
                        'code': u'S1414-81452012000300003',
                        'title': u'title pt',
                        'issn': u'1414-8145',
                        'source': u'Escola Anna Nery',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1414-81452012000300003'
                    }
                ]
            }

        self.assertEqual(controller.query_by_doi(mock_coll, '10.1161/01.res.59.2.178'), expected)

    def test_query_by_doi_invalid_document(self):
        mock_load_article_title_keys = self.mocker.replace(controller.load_document_meta_from_crossref)
        mock_load_article_title_keys(ANY)
        self.mocker.result(None)

        mock_coll = self.mocker.mock()
        self.mocker.replay()

        self.assertEqual(controller.query_by_doi(mock_coll, '10.1161/01.res.59.2.178'), None)

    def test_load_document_meta_from_crossref(self):
        mock_load_article_title_keys = self.mocker.replace('urllib2')
        mock_load_article_title_keys.urlopen(ANY).read()
        self.mocker.result(json.dumps(fixtures.doi_response))
        self.mocker.replay()

        document_meta = controller.load_document_meta_from_crossref('10.1161/01.res.59.2.178')

        self.assertEqual(document_meta, fixtures.doi_response[0])

    def test_load_document_meta_from_crossref_without_title(self):
        response = [
          {
            "doi": u"http://dx.doi.org/10.1161/01.res.59.2.178",
            "score": 18.42057,
            "normalizedScore": 100,
            "fullCitation": u"M. Pagani, F. Lombardi, S. Guzzetti, O. Rimoldi, R. Furlan, P. Pizzinelli, G. Sandrone, G. Malfatto, S. Dell'Orto, E. Piccaluga, 1986, 'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog', <i>Circulation Research</i>, vol. 59, no. 2, pp. 178-193",
            "coins": u"ctx_ver=Z39.88-2004&amp;rft_id=info%3Adoi%2Fhttp%3A%2F%2Fdx.doi.org%2F10.1161%2F01.res.59.2.178&amp;rfr_id=info%3Asid%2Fcrossref.org%3Asearch&amp;rft.atitle=Power+spectral+analysis+of+heart+rate+and+arterial+pressure+variabilities+as+a+marker+of+sympatho-vagal+interaction+in+man+and+conscious+dog&amp;rft.jtitle=Circulation+Research&amp;rft.date=1986&amp;rft.volume=59&amp;rft.issue=2&amp;rft.spage=178&amp;rft.epage=193&amp;rft.aufirst=M.&amp;rft.aulast=Pagani&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.au=M.+Pagani&amp;rft.au=+F.+Lombardi&amp;rft.au=+S.+Guzzetti&amp;rft.au=+O.+Rimoldi&amp;rft.au=+R.+Furlan&amp;rft.au=+P.+Pizzinelli&amp;rft.au=+G.+Sandrone&amp;rft.au=+G.+Malfatto&amp;rft.au=+S.+Dell%27Orto&amp;rft.au=+E.+Piccaluga",
            "year": u"1986"
          }
        ]

        mock_load_article_title_keys = self.mocker.replace('urllib2')
        mock_load_article_title_keys.urlopen(ANY).read()
        self.mocker.result(json.dumps(response))
        self.mocker.replay()

        document_meta = controller.load_document_meta_from_crossref('10.1161/01.res.59.2.178')

        self.assertEqual(document_meta, None)

    def test_load_document_meta_from_crossref_title_equal_None(self):
        response = [
          {
            "doi": u"http://dx.doi.org/10.1161/01.res.59.2.178",
            "score": 18.42057,
            "normalizedScore": 100,
            "fullCitation": u"M. Pagani, F. Lombardi, S. Guzzetti, O. Rimoldi, R. Furlan, P. Pizzinelli, G. Sandrone, G. Malfatto, S. Dell'Orto, E. Piccaluga, 1986, 'Power spectral analysis of heart rate and arterial pressure variabilities as a marker of sympatho-vagal interaction in man and conscious dog', <i>Circulation Research</i>, vol. 59, no. 2, pp. 178-193",
            "coins": u"ctx_ver=Z39.88-2004&amp;rft_id=info%3Adoi%2Fhttp%3A%2F%2Fdx.doi.org%2F10.1161%2F01.res.59.2.178&amp;rfr_id=info%3Asid%2Fcrossref.org%3Asearch&amp;rft.atitle=Power+spectral+analysis+of+heart+rate+and+arterial+pressure+variabilities+as+a+marker+of+sympatho-vagal+interaction+in+man+and+conscious+dog&amp;rft.jtitle=Circulation+Research&amp;rft.date=1986&amp;rft.volume=59&amp;rft.issue=2&amp;rft.spage=178&amp;rft.epage=193&amp;rft.aufirst=M.&amp;rft.aulast=Pagani&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.au=M.+Pagani&amp;rft.au=+F.+Lombardi&amp;rft.au=+S.+Guzzetti&amp;rft.au=+O.+Rimoldi&amp;rft.au=+R.+Furlan&amp;rft.au=+P.+Pizzinelli&amp;rft.au=+G.+Sandrone&amp;rft.au=+G.+Malfatto&amp;rft.au=+S.+Dell%27Orto&amp;rft.au=+E.+Piccaluga",
            "year": u"1986",
            "title": None
          }
        ]

        mock_load_article_title_keys = self.mocker.replace('urllib2')
        mock_load_article_title_keys.urlopen(ANY).read()
        self.mocker.result(json.dumps(response))
        self.mocker.replay()

        document_meta = controller.load_document_meta_from_crossref('10.1161/01.res.59.2.178')

        self.assertEqual(document_meta, None)

    def test_load_document_meta_from_crossref_without_retrieved_document(self):
        mock_load_article_title_keys = self.mocker.replace('urllib2')
        mock_load_article_title_keys.urlopen(ANY).read()
        self.mocker.result('[]')
        self.mocker.replay()

        document_meta = controller.load_document_meta_from_crossref('10.1161/01.res.59.2.178')

        self.assertEqual(document_meta, None)

    def test_load_document_meta(self):

        article = Article(fixtures.article)

        expected = {'code': u'S0101-31222002000100038',
                    'title': u'Estratégias de luta das enfermeiras da Maternidade Leila Diniz para implantação de um modelo humanizado de assistência ao parto',
                    'issn': u'0101-3122',
                    'source': u'Revista Brasileira de Sementes',
                    'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0101-31222002000100038'}

        article_meta = controller.load_document_meta(article)

        self.assertEqual(article_meta, expected)

    def test_remove_accents(self):

        self.assertEqual(controller.remove_accents(u'á, b c de F'), u'abcdef')

    def test_load_article(self):
        mock_coll = self.mocker.mock()
        mock_coll.find_one(ANY, ANY)
        self.mocker.result(fixtures.article)
        self.mocker.replay()

        article = controller.load_article(mock_coll, u'S0101-31222002000100038')

        self.assertEqual(article.original_title(), u'Estratégias de luta das enfermeiras da Maternidade Leila Diniz para implantação de um modelo humanizado de assistência ao parto')

    def test_load_article_invalid_article_id(self):
        mock_coll = self.mocker.mock()
        mock_coll.find_one(ANY, ANY)
        self.mocker.result(None)
        self.mocker.replay()

        article = controller.load_article(mock_coll, u'S0101-31222002000100038')

        self.assertEqual(article, None)

    def test_load_article_title_keys(self):

        article = Article(fixtures.article)

        expected = [u'estrategiasdelutadasenfermeirasdamaternidadeleiladinizparaimplantacaodeummodelohumanizadodeassistenciaaoparto',
                    u'nursingfightingstrategiesintheleiladinizmaternitytowardstheimplantationofahumanizedmodelfordeliverycare',
                    u'estrategiasdeluchadelasenfermerasdelamaternidadleiladinizparalaimplantaciondeunmodelohumanizadodeasistenciaalparto']

        result = controller.load_article_title_keys(article)

        self.assertTrue(u'estrategiasdelutadasenfermeirasdamaternidadeleiladinizparaimplantacaodeummodelohumanizadodeassistenciaaoparto' in result)
        self.assertTrue(u'nursingfightingstrategiesintheleiladinizmaternitytowardstheimplantationofahumanizedmodelfordeliverycare' in result)
        self.assertTrue(u'estrategiasdeluchadelasenfermerasdelamaternidadleiladinizparalaimplantaciondeunmodelohumanizadodeasistenciaalparto' in result)

    def test_query_by_pid(self):
        article = Article(fixtures.article)

        mock_load_article_title_keys = self.mocker.replace(controller.load_article)
        mock_load_article_title_keys(ANY, ANY)
        self.mocker.result(article)

        mock_coll = self.mocker.mock()
        mock_coll.find(ANY, ANY)
        self.mocker.result(fixtures.articles)
        self.mocker.replay()

        expected = { 
                'article':{
                        'code': u'S0101-31222002000100038',
                        'title': u'Estratégias de luta das enfermeiras da Maternidade Leila Diniz para implantação de um modelo humanizado de assistência ao parto',
                        'issn': u'0101-3122',
                        'source': u'Revista Brasileira de Sementes',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0101-31222002000100038'
                },
                'cited_by':[{
                        'code': u'S0104-07072013000100023',
                        'title': u'title en',
                        'issn': u'0104-0707',
                        'source': u'Texto & Contexto - Enfermagem',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-07072013000100023'
                    },{
                        'code': u'S1414-81452012000300003',
                        'title': u'title pt',
                        'issn': u'1414-8145',
                        'source': u'Escola Anna Nery',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1414-81452012000300003'
                    }
                ]
            }
        self.assertEqual(controller.query_by_pid(mock_coll, 'S0101-31222002000100038'), expected)

    def test_query_by_pid_invalid_article_pid(self):
        mock_load_article_title_keys = self.mocker.replace(controller.load_article)
        mock_load_article_title_keys(ANY, ANY)
        self.mocker.result(None)

        mock_coll = self.mocker.mock()
        self.mocker.replay()

        self.assertEqual(controller.query_by_pid(mock_coll, 'S0101-31222002000100038'), None)

    def test_query_by_pid_without_cited_by(self):
        article = Article(fixtures.article)

        mock_load_article_title_keys = self.mocker.replace(controller.load_article)
        mock_load_article_title_keys(ANY, ANY)
        self.mocker.result(article)

        mock_coll = self.mocker.mock()
        mock_coll.find(ANY, ANY)
        self.mocker.result(None)
        self.mocker.replay()

        expected = { 
                'article':{
                        'code': u'S0101-31222002000100038',
                        'title': u'Estratégias de luta das enfermeiras da Maternidade Leila Diniz para implantação de um modelo humanizado de assistência ao parto',
                        'issn': u'0101-3122',
                        'source': u'Revista Brasileira de Sementes',
                        'url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0101-31222002000100038'
                },
                'cited_by': None
            }

        self.assertEqual(controller.query_by_pid(mock_coll, 'S0101-31222002000100038'), expected)


class SingletonMixinTests(MockerTestCase):

    def test_without_args(self):
        class Foo(utils.SingletonMixin):
            pass

        self.assertIs(Foo(), Foo())

    def test_single_int_arg(self):
        class Foo(utils.SingletonMixin):
            def __init__(self, x):
                self.x = x

        self.assertIs(Foo(2), Foo(2))

    def test_single_int_kwarg(self):
        class Foo(utils.SingletonMixin):
            def __init__(self, x=None):
                self.x = x

        self.assertIs(Foo(x=2), Foo(x=2))

    def test_multiple_int_arg(self):
        class Foo(utils.SingletonMixin):
            def __init__(self, x, y):
                self.x = x
                self.y = y

        self.assertIs(Foo(2, 6), Foo(2, 6))

    def test_multiple_int_kwarg(self):
        class Foo(utils.SingletonMixin):
            def __init__(self, x=None, y=None):
                self.x = x
                self.y = y

        self.assertIs(Foo(x=2, y=6), Foo(x=2, y=6))

    def test_ConfigParser_arg(self):
        class Foo(utils.SingletonMixin):
            def __init__(self, x):
                self.x = x

        settings = ConfigParser.ConfigParser()
        self.assertIs(
            Foo(settings),
            Foo(settings)
        )


class ConfigurationTests(MockerTestCase):

    def _make_fp(self):
        mock_fp = self.mocker.mock()

        mock_fp.name
        self.mocker.result('settings.ini')

        mock_fp.readline()
        self.mocker.result('[app]')

        mock_fp.readline()
        self.mocker.result('status = True')

        mock_fp.readline()
        self.mocker.result('')

        self.mocker.replay()

        return mock_fp

    def test_fp(self):
        mock_fp = self._make_fp()
        conf = utils.Configuration(mock_fp)
        self.assertEqual(conf.get('app', 'status'), 'True')

    def test_non_existing_option_raises_ConfigParser_NoOptionError(self):
        mock_fp = self._make_fp()
        conf = utils.Configuration(mock_fp)
        self.assertRaises(
            ConfigParser.NoOptionError,
            lambda: conf.get('app', 'missing'))

    def test_non_existing_section_raises_ConfigParser_NoSectionError(self):
        mock_fp = self._make_fp()
        conf = utils.Configuration(mock_fp)
        self.assertRaises(
            ConfigParser.NoSectionError,
            lambda: conf.get('missing', 'status'))

