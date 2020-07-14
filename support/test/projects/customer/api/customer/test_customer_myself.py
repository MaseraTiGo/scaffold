# coding=UTF-8

import os
import json

from support.common.testcase.api_test_case import APITestCase


class CustomerTestCase(APITestCase):

    def setUp(self):
        self.update_info = {
            'name': '王海东',
            'gender': 'woman',
            'birthday': '1987-07-07',
            'phone': '15527703110',
            'email': '15527701001@qq.com',
            'wechat': '155277701001',
            'qq': '1522313132',
            'education': 'high',
        }

    def tearDown(self):
        pass

    def assert_customer_fields(self, customer, need_id = False):
        if need_id:
            self.assertTrue('id' in customer)
        self.assertTrue('name' in customer)
        self.assertTrue('gender' in customer)
        self.assertTrue('birthday' in customer)
        self.assertTrue('phone' in customer)
        self.assertTrue('email' in customer)
        self.assertTrue('wechat' in customer)
        self.assertTrue('qq' in customer)

    def test_customer_myself_get(self):
        api = 'customer.myself.get'
        result = self.access_customer_api(api)
        self.assertTrue('customer_info' in result)
        self.assert_customer_fields(result['customer_info'])

    def test_customer_myself_update(self):
        api = "customer.myself.update"
        self.access_customer_api(api = api, myself_info = json.dumps(self.update_info))
