# coding=UTF-8

import os
import json
import hashlib

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class StaffAccountTest(CrmAPITestCase):

    def setUp(self):
        username = ''
        password = ''

    def tearDown(self):
        pass
    '''
    def test_account_login(self):
        api = 'staff.account.login'
        params = {
            'username': 'admin',
            "password": hashlib.md5("123456".encode('utf8')).hexdigest(),
        }
        result = self.access_api(api = api, is_auth = False, **params)
        self.assertTrue('access_token' in result)
        self.assertTrue('renew_flag' in result)
        self.assertTrue('expire_time' in result)


    def test_account_logout(self):
        api = 'staff.account.logout'
        params = {}
        self.access_api(api = api, **params)

    def test_account_password_modify(self):
        api = 'staff.account.password.modify'
        password = hashlib.md5("123456".encode('utf8')).hexdigest()
        self.access_api(api = api, old_password = password, \
                        new_password = password, repeat_password = password)
    '''
    def test_account_create(self):
        api = 'staff.account.add'
        staff_id = 4
        account_info = json.dumps({
            "username":"15527703111",
            "status":"enable"
        })
        self.access_api(api = api, staff_id = staff_id, \
                        account_info = account_info)