# coding=UTF-8
import json
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerContractTest(CustomerAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_contract_create(self):
        api = 'customer.contract.add'
        order_item_id = 25
        result = self.access_api(
            api = api,
            order_item_id = order_item_id
        )
        print("====>>>>", result["contract_info"])
        self.assertTrue('contract_info' in result)
    '''
    def test_product_goods_get(self):
        api = 'customer.contract.get'
        params = {
            "order_item_id": 1
        }
        result = self.access_api(api = api, **params)
        print(result)
        self.assertTrue('contract_list' in result)
    '''