# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase
from support.common.generator.field.model.entity import CustomerEntity


class CustomerAddressTestCase(CrmAPITestCase):

    def setUp(self):
        self.customer = CustomerEntity().calc()

    def tearDown(self):
        pass

    def assert_customer_address_fields(self, address, need_id = False):
        if need_id:
            self.assertTrue('id' in address)
        self.assertTrue('contacts' in address)
        self.assertTrue('gender' in address)
        self.assertTrue('phone' in address)
        self.assertTrue('city' in address)
        self.assertTrue('address' in address)
        self.assertTrue('is_default' in address)
        self.assertTrue('create_time' in address)

    def test_search_customer_address(self):
        api = 'customer.address.search'
        customer_id = self.customer.id
        result = self.access_api(
            api = api,
            customer_id = customer_id,
        )
        self.assertTrue("data_list" in result)
        for address in result['data_list']:
            self.assert_customer_address_fields(address, True)
