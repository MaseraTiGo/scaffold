# coding=UTF-8

import unittest

from sys.core.field.base import BaseField


class TestField(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_api_field(self):
        """ test field """
        class t(object):
            a = BaseField(name = "yrk", desc = "hahahahhaha")

        test = t()
        test.a = 10

        t2 = t()
        t2.a = 20

        print(test.a)
        print(t2.a)

