# coding: utf-8

from mocker import Mocker
import mocker
import unittest
import ConfigParser
import json

from mocker import ANY, MockerTestCase
from xylose.scielodocument import Article

from citedby import utils
from citedby import controller
import fixtures


class ControllerTests(mocker.MockerTestCase):

    def test_remove_accents(self):

        self.assertEqual(controller.remove_accents(u'á, b c de F'), u'abcdef')

    def test_load_article_title_keys(self):

        article = Article(fixtures.article)

        expected = [u'estrategiasdelutadasenfermeirasdamaternidadeleiladinizparaimplantacaodeummodelohumanizadodeassistenciaaoparto',
                    u'nursingfightingstrategiesintheleiladinizmaternitytowardstheimplantationofahumanizedmodelfordeliverycare',
                    u'estrategiasdeluchadelasenfermerasdelamaternidadleiladinizparalaimplantaciondeunmodelohumanizadodeasistenciaalparto']

        self.assertEqual(controller.load_article_title_keys(article), expected)

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
                        'journal': u'Revista Brasileira de Sementes',
                        'article_url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0101-31222002000100038'
                },
                'cited_by':[{
                        'code': u'S0104-07072013000100023',
                        'title': u'title en',
                        'issn': u'0104-0707',
                        'journal': u'Texto & Contexto - Enfermagem',
                        'article_url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-07072013000100023'
                    },{
                        'code': u'S1414-81452012000300003',
                        'title': u'title pt',
                        'issn': u'1414-8145',
                        'journal': u'Escola Anna Nery',
                        'article_url': u'http://www.scielo.br/scielo.php?script=sci_arttext&pid=S1414-81452012000300003'
                    }
                ]
            }
        self.assertEqual(controller.query_by_pid(mock_coll, 'S0101-31222002000100038'), expected)

class SingletonMixinTests(mocker.MockerTestCase):

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


class ConfigurationTests(mocker.MockerTestCase):

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

