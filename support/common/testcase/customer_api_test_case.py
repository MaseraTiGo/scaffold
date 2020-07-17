# coding=UTF-8

'''
Created on 2016年8月3日

@author: Administrator
'''

# import python standard package
import hashlib
import support.test_settings
from support.common.testcase.api_test_case import APITestCase


class CustomerAPITestCase(APITestCase):

    ACCESS_FLAG = "customer-mobile"
    _test_url = "http://localhost:{}/interface/".format(
        support.test_settings.TEST_PORT
    )

    def get_auth_token(self):
        api = "customer.account.login"
        username = "15527703115"  # "15623937796"
        password = hashlib.md5("123456".encode('utf8')).hexdigest()
        result = self.access_api(
            api=api,
            is_auth=False,
            username=username,
            password=password
        )
        self._auth_token = result['access_token']
        self._renew_flag = result['renew_flag']

    def renew_token(self):
        api = 'customer.account.token.renew'
        params = {
            'auth_token': self._auth_token,
            'renew_flag': self._renew_flag,
        }
        result = self.access_api(api=api, is_auth=False, **params)
        self._auth_token = result['access_token']
        self._renew_flag = result['renew_flag']
