# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase
from support.common.generator.field.model.entity import CustomerEntity


class CustomerTransactionTestCase(CrmAPITestCase):

    def setUp(self):
        self.customer=CustomerEntity().calc()

    def tearDown(self):
        pass

    def assert_customer_transaction_fields(self,transaction,need_id=False):
        if need_id:
            self.assertTrue('id' in transaction)
        self.assertTrue('number' in transaction)
        self.assertTrue('amount' in transaction)
        self.assertTrue('pay_type' in transaction)
        self.assertTrue('business_type' in transaction)
        self.assertTrue('remark' in transaction)
        self.assertTrue('create_time' in transaction)

    def test_search_customer_transaction(self):
        api='customer.transaction.search'
        customer_id=self.customer.id
        result=self.access_api(
            api=api,
            current_page=1,
            customer_id=customer_id,
        )
        self.assertTrue("data_list" in result)
        for transaction in result['data_list']:
            self.assert_customer_transaction_fields(transaction,True)
