# coding=UTF-8

import os
import unittest
import json

from abs.middleware.data.register import RegisterImport


class Import(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_import_gjp(self):
        """ test import gjp data"""
        cur_path = os.path.dirname(os.path.abspath(__file__))
        # file_path = os.path.join(cur_path, 'test_1.xlsx')
        file_path = os.path.join(cur_path, 'test.xls')
        f = open(file_path, 'rb').read()
        # print('--------->>>>    ', f)
        gjp = RegisterImport()
        # gjp.run(file_path)
        gjp.run(f)
