# coding=UTF-8

import json

from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerNoticeTest(CustomerAPITestCase):

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def test_account_register(self):
        api = 'message.search'
        params = {
            'current_page': 1,
            'unique_number': 1
        }
        result = self.access_api(api=api, **params)
        print(f'get notice result: \n{result}')
        for item in result.get('data_list', []):
            self.assertTrue('title' in item.keys())
            self.assertTrue('content' in item.keys())
            self.assertTrue('datetime' in item.keys())
