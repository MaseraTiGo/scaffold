# coding=UTF-8

'''
Created on 2016年8月3日

@author: Administrator
'''

import requests
import support.test_settings
from support.common.testcase.api_test_case import APITestCase


class FileAPITestCase(APITestCase):

    ACCESS_FLAG = "file"
    _test_url = "http://localhost:{}/interface/".format(
        support.test_settings.TEST_PORT
    )

    def get_auth_token(self):
        pass

    def renew_token(self):
        pass

    def access_api(self, api, files, **parms):
        access_parms = self._combination_parms(
            flag=self.ACCESS_FLAG,
            api=api,
            **parms
        )
        url = self._get_api_url()
        result = requests.post(url, data=access_parms, files=files)
        return self._get_response_data(result.json())
