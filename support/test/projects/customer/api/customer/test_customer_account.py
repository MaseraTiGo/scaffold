# coding=UTF-8

import os
import json
import hashlib

from support.common.testcase.api_test_case import APITestCase

class CustomerAccountTest(APITestCase):

    def setUp(self):
        self.customer_info = {
            'username': '15527703115',
            "password": hashlib.md5("123456".encode('utf8')).hexdigest(),
        }

    def tearDown(self):
        pass

    def test_account_register(self):
        api = 'customer.account.register'
        params = {
            'phone': self.customer_info['username'],
            "password": self.customer_info['password'],
            "code": '123456'
        }
        result = self.access_customer_api(api = api, is_auth = False, **params)
        self.assertTrue('access_token' in result)
        self.assertTrue('renew_flag' in result)
        self.assertTrue('expire_time' in result)

    def test_account_renew_token(self):
        result = self.test_account_login()
        api = 'customer.account.token.renew'
        params = {
            'auth_token': result['access_token'],
            'renew_flag': result['renew_flag'],
        }

        result = self.access_customer_api(api = api, is_auth = False, **params)
        self.assertTrue('access_token' in result)
        self.assertTrue('renew_flag' in result)
        self.assertTrue('expire_time' in result)

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
        return result

    def test_account_logout(self):
        api = 'customer.account.logout'
        params = {}
        self.access_customer_api(api = api, **params)

    def test_account_password_modify(self):
        api = 'customer.account.password.modify'
        params = {
            "old_password": hashlib.md5("123456".encode('utf8')).hexdigest(),
            "new_password": hashlib.md5("123456".encode('utf8')).hexdigest(),
        }
        self.access_customer_api(api = api, **params)

    def test_account_password_forget(self):
        api = 'customer.account.password.forget'
        params = {
            "password": hashlib.md5("123456".encode('utf8')).hexdigest(),
            "code": "123456",
            "phone": "15527703115",
        }
        self.access_customer_api(api = api, **params)
