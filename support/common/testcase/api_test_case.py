# coding=UTF-8

'''
Created on 2016年8月3日

@author: Administrator
'''

# import python standard package
import time
import json
import unittest
import urllib.request
import support.test_settings

# import thread package

# import my project package
from infrastructure.utils.common.signature import unique_parms,\
        generate_signature


class APITestCase(unittest.TestCase):

    ACCESS_FLAG = ""
    _test_url = "http://localhost:{}/interface/".format(
        support.test_settings.TEST_PORT
    )
    _auth_token = ""
    _renew_flag = ""

    def _get_current_time(self):
        return int(time.time())

    def _generate_signature(self, parms):
        unique_string, length = unique_parms(parms)
        return generate_signature(unique_string, length)

    def _get_api_url(self):
        return self._test_url

    def _combination_parms(self, **kwargs):
        parms = {
                    "timestamp": self._get_current_time()
                 }
        parms.update(kwargs)
        sign = self._generate_signature(parms)
        parms.update({"sign": sign})
        return parms

    def _connect(cls, url, data):
        postdata = urllib.parse.urlencode(data)
        postdata = postdata.encode('utf-8')
        result = ""
        with urllib.request.urlopen(url, postdata) as rep:
            result = rep.read().decode()
        return result

    def _parse(self, response_text):
        return json.loads(response_text)

    def _get_response_data(self, result):
        status = result['status']
        self.assertEqual(status, 'ok', result.get("msg", ""))
        return result['result']

    def access_base(self, flag, api, **parms):
        access_parms = self._combination_parms(flag=flag, api=api, **parms)
        response_text = self._connect(self._get_api_url(), access_parms)
        result = self._parse(response_text)
        return self._get_response_data(result)

    def access_api(self, api, is_auth=True, **parms):
        if is_auth:
            if self._auth_token == "":
                self.get_auth_token()
                self.renew_token()
            parms.update({'auth': self._auth_token})

        return self.access_base(self.ACCESS_FLAG, api, **parms)

    def get_auth_token(self, api, is_auth=True, **parms):
        raise Exception("this interface is need to implement!")

    def renew_token(self, api, is_auth=True, **parms):
        raise Exception("this interface is need to implement!")
