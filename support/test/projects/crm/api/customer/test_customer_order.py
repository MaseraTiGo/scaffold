# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase
from support.common.generator.field.model.entity import CustomerEntity


class CustomerOrderTestCase(CrmAPITestCase):

    def setUp(self):
        self.customer = CustomerEntity().generate()

    def tearDown(self):
        pass

    def assert_customer_order_fields(self, order, need_id = False):
        if need_id:
            self.assertTrue('id' in order)
        self.assertTrue('number' in order)
        self.assertTrue('last_payment_time' in order)
        self.assertTrue('actual_amount' in order)
        self.assertTrue('status' in order)
        self.assertTrue('create_time' in order)

    def test_search_customer_order(self):
        api = 'customer.order.search'
        customer_id = 6
        current_page = 1
        result = self.access_api(
            api = api,
            customer_id = customer_id,
            current_page = current_page
        )
        self.assertTrue("data_list" in result)
        for address in result['data_list']:
            self.assert_customer_order_fields(address, True)
