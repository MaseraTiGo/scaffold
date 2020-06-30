# coding=UTF-8

import os
import json

from support.common.testcase.api_test_case import APITestCase


class CustomerBankcardTestCase(APITestCase):

    def setUp(self):
        self.add_info = {
            'number': '6222020607000847162',
            'phone': '15527701100',
            'name': '胡晓星',
            'identification': '152127188807091121',
            'code': '1234'
        }

    def tearDown(self):
        pass

    def assert_bankcard_fields(self, bankcard):
        self.assertTrue('id' in bankcard)
        self.assertTrue('number' in bankcard)
        self.assertTrue('phone' in bankcard)
        self.assertTrue('name' in bankcard)
        self.assertTrue('identification' in bankcard)

    def test_customer_myself_bankcard_add(self):
        api = 'customer.myself.bankcard.add'
        self.access_customer_api(api, bankcard_info = json.dumps(self.add_info))

    def test_customer_myself_bankcard_all(self):
        api = 'customer.myself.bankcard.all'
        result = self.access_customer_api(api)
        if not result:
            self.test_customer_myself_bankcard_add()
            result = self.access_customer_api(api)

        self.assertTrue("bankcard_list" in result)
        for bankcard in result['bankcard_list']:
            self.assert_bankcard_fields(bankcard)
        return result['bankcard_list']

    def test_customer_myself_bankcard_get(self):
        api = "customer.myself.bankcard.get"
        bankcard_id = self.test_customer_myself_bankcard_all()[-1]['id']
        result = self.access_customer_api(api = api, bankcard_id = bankcard_id)
        self.assertTrue('bankcard_info' in result)
        self.assert_bankcard_fields(result['bankcard_info'])

    def test_customer_myself_bankcard_remove(self):
        api = "customer.myself.bankcard.remove"
        bankcard_id = self.test_customer_myself_bankcard_all()[-1]['id']
        self.access_customer_api(api = api, bankcard_id = bankcard_id)
