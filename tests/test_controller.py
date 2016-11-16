# coding: utf-8
import unittest

from citedby import controller


class ControllerTest(unittest.TestCase):

    def test_get_author_name_forms_1(self):

        result = controller.get_author_name_forms(u'José Afonso Silva')

        expected = sorted([
            'silva jose afonso',
            'jose afonso silva',
            'silva j a'
        ])

        self.assertEqual(sorted(result), expected)

    def test_get_author_name_forms_2(self):

        result = controller.get_author_name_forms('Silva A J')

        expected = sorted(['silva a j'])

        self.assertEqual(sorted(result), expected)

    def test_get_author_name_forms_3(self):

        result = controller.get_author_name_forms(u'José Afonso da Silva')

        expected = sorted([
            'silva jose afonso',
            'jose afonso da silva',
            'silva j a'
        ])

        self.assertEqual(sorted(result), expected)

    def test_get_author_name_forms_4(self):

        result = controller.get_author_name_forms(u'Antonio Rogério Brizante de Vasconcelos')

        expected = sorted([
            'antonio rogerio brizante de vasconcelos',
            'vasconcelos a r b',
            'vasconcelos antonio rogerio brizante']
        )

        self.assertEqual(sorted(result), expected)
