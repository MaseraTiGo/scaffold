# coding=UTF-8

import json

from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerNoticeTest(CustomerAPITestCase):

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def test_customer_notice_search(self):
        api = 'notice.search'
        params = {'current_page': 1}
        result = self.access_api(api=api, **params)
        for item in result.get('data_list', []):
            self.assertTrue('title' in item.keys())
            self.assertTrue('content' in item.keys())
            self.assertTrue('create_time' in item.keys())
