# coding=UTF-8

from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerAccountTest(CustomerAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_account_phone_verification_code(self):
        api = 'customer.account.vcode.phone'
        params = {
            "number": "15827054862",
            'sms_type': 'register'
        }
        self.access_api(api=api, is_auth=False, **params)

    def test_account_image_verification_code(self):
        api = 'customer.account.vcode.image'
        params = {}
        result = self.access_api(api=api, is_auth=False, **params)
        self.assertTrue('code' in result)
