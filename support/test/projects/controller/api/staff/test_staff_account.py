# coding=UTF-8

import json
import hashlib

from support.common.testcase.controller_api_test_case import \
        ControllerAPITestCase


class StaffAccountTest(ControllerAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_account_fiels(self, account_info):
        self.assertTrue('username' in account_info)
        self.assertTrue('nick' in account_info)
        self.assertTrue('head_url' in account_info)
        self.assertTrue('last_login_time' in account_info)
        self.assertTrue('last_login_ip' in account_info)
        self.assertTrue('register_ip' in account_info)
        self.assertTrue('status' in account_info)
        self.assertTrue('update_time' in account_info)
        self.assertTrue('create_time' in account_info)

    def test_account_login(self):
        api = 'staff.account.login'
        params = {
            'username': 'yanfav5',
            "password": hashlib.md5("123456".encode('utf8')).hexdigest(),
        }
        result = self.access_api(api=api, is_auth=False, **params)
        self.assertTrue('access_token' in result)
        self.assertTrue('renew_flag' in result)
        self.assertTrue('expire_time' in result)

    def test_account_logout(self):
        api = 'staff.account.logout'
        params = {}
        self.access_api(api=api, **params)

    def test_account_get(self):
        api = 'staff.account.get'
        result = self.access_api(api=api)
        self.assertTrue('account_info' in result)
        self.assert_account_fiels(result['account_info'])

    def test_account_update(self):
        api = 'staff.account.update'
        update_info = {
            'nick': "我是流氓我怕谁",
            'head_url': "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1597232346269&di=003269ea6aa55de935f180b98f5d1222&imgtype=0&src=http%3A%2F%2Fhbimg.b0.upaiyun.com%2F6e8f56b2543cce8bffa35b22d03684fae76a1b2c56c32-COdswi_fw658",

        }
        self.access_api(
            api=api,
            update_info=json.dumps(update_info)
        )

    def test_account_password_modify(self):
        api = 'staff.account.password.modify'
        password = hashlib.md5("123456".encode('utf8')).hexdigest()
        self.access_api(
            api=api,
            old_password=password,
            new_password=password,
            repeat_password=password
        )

    def test_account_phone_verification_code(self):
        api = 'staff.account.vcode.phone'
        params = {
            "number": "15527703115",
        }
        result = self.access_api(api=api, is_auth=False, **params)
        self.assertTrue('code' in result)

    def test_account_image_verification_code(self):
        api = 'staff.account.vcode.image'
        params = {}
        result = self.access_api(api=api, is_auth=False, **params)
        self.assertTrue('code' in result)
