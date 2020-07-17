# coding=UTF-8

import json
import random

from support.generator.field.model import PayTypeConstant
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerTransactionTestCase(CustomerAPITestCase):

    def setUp(self):
        self.add_info = {
            'bank_number': '6222020607000847162',
            'phone': '15527701100',
            'name': '胡晓星',
            'identification': '152127188807091121',
            'code': '1234'
        }

    def tearDown(self):
        pass

    def assert_transaction_fields(self, transaction, is_detail=False):
        self.assertTrue('id' in transaction)
        self.assertTrue('number' in transaction)
        self.assertTrue('amount' in transaction)
        self.assertTrue('pay_type' in transaction)
        self.assertTrue('remark' in transaction)
        self.assertTrue('create_time' in transaction)
        if is_detail:
            self.assertTrue('status' in transaction)

    def test_customer_balance_get(self):
        api = 'customer.finance.balance.get'
        result = self.access_api(api)
        self.assertTrue('balance' in result)

    def test_customer_topup(self):
        api = 'customer.finance.balance.topup'
        self.access_api(
            api,
            amount=random.randint(1000000, 99999999),
            pay_type=PayTypeConstant().generate(),
            remark="测试余额充值",
        )

    def test_customer_withdraw(self):
        self.test_customer_topup()
        api = 'customer.finance.balance.withdraw'
        self.access_api(
            api,
            amount=0 - random.randint(1, 100),
            pay_type=PayTypeConstant().generate(),
            remark="测试余额提现",
        )

    def test_customer_transaction_search(self):
        api = 'customer.finance.transaction.search'
        result = self.access_api(
            api,
            current_page=1,
            search_info=json.dumps({}),
        )

        self.assertTrue('data_list' in result)
        self.assertTrue('total' in result)
        self.assertTrue('total_page' in result)
        if not result['data_list']:
            for _ in range(100):
                if random.randint(1, 5) % 2 == 0:
                    self.test_customer_topup()
                if random.randint(1, 5) % 2 == 0:
                    self.test_customer_topup()
            result = self.access_api(
                api,
                current_page=0,
                search_info=json.dumps({}),
            )

        self.assertTrue('data_list' in result)
        for transaction in result['data_list']:
            self.assert_transaction_fields(transaction)
        return result['data_list']

    def test_customer_transaction_get(self):
        api = "customer.finance.transaction.get"
        transaction_id = self.test_customer_transaction_search()[-1]['id']
        result = self.access_api(api=api, transaction_id=transaction_id)
        self.assertTrue('transaction_info' in result)
        self.assert_transaction_fields(result['transaction_info'])

    def test_customer_transaction_statistics_montyly(self):
        api = "customer.finance.transaction.statistics.monthly"
        result = self.access_api(api=api)
        self.assertTrue('statistics_list' in result)
        for statistics in result['statistics_list']:
            self.assertTrue('year' in statistics)
            self.assertTrue('month' in statistics)
            self.assertTrue('income' in statistics)
            self.assertTrue('expense' in statistics)
