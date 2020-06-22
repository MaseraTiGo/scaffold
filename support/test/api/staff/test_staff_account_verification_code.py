# coding=UTF-8

import os
import json
import hashlib

from support.common.testcase.api_test_case import APITestCase

class StaffAccountTest(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_account_phone_verification_code(self):
        api = 'staff.account.vcode.phone'
        params = {
            "number": "15527703115",
        }
        result = self.access_crm_api(api = api, is_auth = False, **params)
        self.assertTrue('code' in result)

    def test_account_image_verification_code(self):
        api = 'staff.account.vcode.image'
        params = {}
        result = self.access_crm_api(api = api, is_auth = False, **params)
        self.assertTrue('code' in result)
