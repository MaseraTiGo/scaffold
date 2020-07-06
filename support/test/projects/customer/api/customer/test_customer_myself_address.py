# coding=UTF-8

import os
import json

from support.common.testcase.api_test_case import APITestCase


class CustomerAddressTestCase(APITestCase):

    def setUp(self):
        self.add_info = {
            'contacts': '杨荣凯',
            'gender': 'man',
            'phone': '15527701100',
            'city': '湖北省-武汉市-青山区',
            'address': '光谷软件园展示中心C做3楼',
            'is_default': True,
        }
        self.update_info = {
            'contacts': '胡世刚',
            'gender': 'woman',
            'phone': '15527701111',
            'city': '湖北省-武汉市-洪山区',
            'address': '光谷软件园展示中心C做3楼301',
            'is_default': True,
        }

    def tearDown(self):
        pass

    def assert_address_fields(self, address):
        self.assertTrue('id' in address)
        self.assertTrue('contacts' in address)
        self.assertTrue('gender' in address)
        self.assertTrue('phone' in address)
        self.assertTrue('city' in address)
        self.assertTrue('address' in address)
        self.assertTrue('is_default' in address)

    def test_customer_myself_address_add(self):
        api = 'customer.myself.address.add'
        self.access_customer_api(api, address_info = json.dumps(self.add_info))

    def test_customer_myself_address_all(self):
        api = 'customer.myself.address.all'
        result = self.access_customer_api(api)
        self.assertTrue("address_list" in result)
        if not result['address_list']:
            self.test_customer_myself_address_add()
            result = self.access_customer_api(api)

        for address in result['address_list']:
            self.assert_address_fields(address)
        return result['address_list']

    def test_customer_myself_address_get(self):
        api = "customer.myself.address.get"
        address_id = self.test_customer_myself_address_all()[-1]['id']
        result = self.access_customer_api(api = api, address_id = address_id)
        self.assertTrue('address_info' in result)
        self.assert_address_fields(result['address_info'])

    def test_customer_myself_address_update(self):
        api = "customer.myself.address.update"
        address_id = self.test_customer_myself_address_all()[-1]['id']
        self.access_customer_api(api = api, address_id = address_id, update_info = json.dumps(self.update_info))

    def test_customer_myself_address_remove(self):
        api = "customer.myself.address.remove"
        address_id = self.test_customer_myself_address_all()[-1]['id']
        self.access_customer_api(api = api, address_id = address_id)
