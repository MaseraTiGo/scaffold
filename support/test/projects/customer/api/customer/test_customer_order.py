# coding=UTF-8
import json
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerOrderTest(CustomerAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_goods_all(self):
        api = 'customer.order.add'
        order_info = json.dumps({
            'strike_price': 5555,
            'address_id': 1,
            'goods_list': [
                {
                    'quantity': 2,
                    'specification_id': 1
                }
            ]
        })
        self.access_api(api=api, order_info=order_info)
