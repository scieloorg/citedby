# coding: utf-8
import unittest

from proc import loaddata

class LoaddataTest(unittest.TestCase):

    def test_cleanup_string_1(self):

        result = loaddata.cleanup_string(u'Revista de Saúde Pública')

        expected = u'revista de saude publica'

        self.assertEqual(result, expected)

    def test_cleanup_string_2(self):

        result = loaddata.cleanup_string(u'Rev. de Saúde Púb')

        expected = u'rev de saude pub'

        self.assertEqual(result, expected)

    def test_cleanup_string_3(self):

        result = loaddata.cleanup_string(u'Rev. de Saúde (Púb)')

        expected = u'rev de saude pub'

        self.assertEqual(result, expected)
