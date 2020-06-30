# coding=UTF-8

import os
import json
import hashlib

from support.common.testcase.api_test_case import APITestCase

class CustomerAccountTest(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_account_login(self):
        api = 'customer.account.login'
        params = {
            'username': '15527703115',
            "password": hashlib.md5("123456".encode('utf8')).hexdigest(),
        }
        result = self.access_customer_api(api = api, is_auth = False, **params)
        self.assertTrue('access_token' in result)
        self.assertTrue('renew_flag' in result)
        self.assertTrue('expire_time' in result)


    def test_account_logout(self):
        api = 'customer.account.logout'
        params = {}
        self.access_customer_api(api = api, **params)
