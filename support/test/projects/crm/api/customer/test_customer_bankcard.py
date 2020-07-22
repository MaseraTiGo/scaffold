# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase
from support.common.generator.field.model.entity import CustomerEntity


class CustomerBankcardTestCase(CrmAPITestCase):

    def setUp(self):
        self.customer = CustomerEntity().calc()

    def tearDown(self):
        pass

    def assert_customer_bankcard_fields(self, bankcard, need_id = False):
        if need_id:
            self.assertTrue('id' in bankcard)
        self.assertTrue('bank_name' in bankcard)
        self.assertTrue('bank_code' in bankcard)
        self.assertTrue('bank_number' in bankcard)
        self.assertTrue('name' in bankcard)
        self.assertTrue('phone' in bankcard)
        self.assertTrue('identification' in bankcard)
        self.assertTrue('create_time' in bankcard)

    def test_search_customer_bankcard(self):
        api = 'customer.bankcard.search'
        customer_id = self.customer.id
        result = self.access_api(
            api = api,
            customer_id = customer_id,
        )
        self.assertTrue("data_list" in result)
        for bankcard in result['data_list']:
            self.assert_customer_bankcard_fields(bankcard, True)
