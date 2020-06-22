# coding=UTF-8

import unittest
import json

from agile.server.app.base import user_service
from agile.protocol.base import TestProtocol


class TestUserServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_api_flowwork(self):
        """ test api flowwork"""
        j = json.dumps({'c1':'11111','c2':2222})
        l2 = json.dumps([{'c1':'12111','c2':1222},{'c1':'31111','c2':3222}])
        l = json.dumps(['11', '22', '33', '44'])

        data = {'flag':'user','api':'agile.apis.user.customer.testapi', 'yrk':'a', 'data':j,
                'data_list':l, 'data_list_1':l2}
        p = TestProtocol()
        p.add(user_service)
        p.run(data)
        print('hahahhaha')
