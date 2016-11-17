# coding: utf-8

import unittest

from citedby import utils


class UtilsTest(unittest.TestCase):

    def test_cleanup_string_1(self):

        result = utils.cleanup_string(u"Teste ÁÉÍÓÚáéíóú#@$%^ˆ&*()")

        self.assertEqual('teste aeiouaeiou', result)

    def test_cleanup_string_2(self):

        result = utils.cleanup_string(u"increase in skeletal muscle protein content by the ß selective adrenergic agonist clenbuterol exacerbates hypoalbuminemia in rats fed a lowprotein diet")

        self.assertEqual('increase in skeletal muscle protein content by the  selective adrenergic agonist clenbuterol exacerbates hypoalbuminemia in rats fed a lowprotein diet', result)
