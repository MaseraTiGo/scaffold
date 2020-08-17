# coding=UTF-8

import json

from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerAccountTest(CustomerAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_account_register(self):
        api = 'adsense.advertisement.search'
        params = {
            'search_info': json.dumps({
                'label': 'index_banner'
            })
        }
        result = self.access_api(api=api, is_auth=False, **params)
        print(result)
        self.assertTrue('data_list' in result)