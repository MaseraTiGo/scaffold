# coding=UTF-8

'''
Created on 2016年8月3日

@author: Administrator
'''

import support.test_settings
from support.common.testcase.api_test_case import APITestCase


class MiddlegroundAPITestCase(APITestCase):

    ACCESS_FLAG = "middleground"
    _test_url = "http://localhost:{}/interface/".format(
        support.test_settings.TEST_PORT
    )

    def get_auth_token(self):
        pass

    def renew_token(self):
        pass

    def access_api(self, api, **parms):
        return super(MiddlegroundAPITestCase, self).access_api(
            api,
            False,
            **parms
        )
