# coding=UTF-8

import os
import json

from support.common.testcase.api_test_case import APITestCase

class CustomerTestCase(APITestCase):

    def setUp(self):
        self.customer_info = {
            'name': '杨荣凯',
            'gender': 'man',
            'birthday': '1990-07-07',
            'phone': '15527703115',
            'email': '15527703115@qq.com',
            'wechat': '15527703115',
            'qq': '15527703115',
            'education': 'high',
        }
        
        self.update_info = {
            'name': '王海东',
            'gender': 'man',
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
        self.assertTrue('education' in customer)

    def test_create_customer(self):
        api = 'customer.add'
        self.access_crm_api(api = api, customer_info = json.dumps(self.customer_info))

    def test_search_customer(self):
        api = 'customer.search' 
        current_page = 1
        result = self.access_crm_api(api = api, current_page = current_page, search_info = json.dumps({}))
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        for customer in result['data_list']:
            self.assert_customer_fields(customer, True)
        return result['data_list']

    def test_get_customer(self):
        customer_list = self.test_search_customer()
        if customer_list:
            customer_id = customer_list[-1]['id']
            api = "customer.get"
            result = self.access_crm_api(api = api, customer_id = customer_id)
            self.assertTrue('customer_info' in result)
            self.assert_customer_fields(result['customer_info'])
        else:
            self.assertTrue("the customer_id cann't acquired! " == "")

    def test_update_customer(self):
        customer_list = self.test_search_customer()
        if customer_list:
            customer_id = customer_list[-1]['id']
            api = "customer.update"
            self.access_crm_api(api = api, customer_id = customer_id, customer_info =
                                         json.dumps(self.update_info))
        else:
            self.assertTrue("the customer_id cann't acquired! " == "")
