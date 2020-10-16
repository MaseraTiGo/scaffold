# coding=UTF-8

import random
import hashlib

from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerAccountTest(CustomerAPITestCase):

    def setUp(self):
        self.customer_info = {
            'username': '15527703115',
            "password": hashlib.md5("123456".encode('utf8')).hexdigest(),
        }

    def tearDown(self):
        pass

    def test_wechat_register(self):
        api = 'customer.account.wechatregister'
        params = {
            # 'client_type': 'ios',
            '_clientType': 'ios',
            "access_token": '25000000000000',
            "open_id": '25000000000000',
            "phone": '13139069019',
            'unique_code': '250250',
            'verify_code': '250250',
        }
        result = self.access_api(api=api, is_auth=False, **params)
        print('result is ============>', result)
        self.assertTrue('access_token' in result)
        self.assertTrue('renew_flag' in result)
        self.assertTrue('expire_time' in result)

    # def test_wechat_login(self):
    #     api = 'customer.account.wechatlogin'
    #     params = {
    #         'code': 'otrJK5zP3VVRaFXbQuqcA6E75DTU',
    #     }
    #
    #     result = self.access_api(api=api, is_auth=False, **params)
    #     print('result is =============>', result)
    #     self.assertTrue('access_token' in result)
    #     self.assertTrue('renew_flag' in result)
    #     # self.assertTrue('expire_time' in result)
