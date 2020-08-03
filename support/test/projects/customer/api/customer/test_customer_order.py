# coding=UTF-8
import json
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerOrderTest(CustomerAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order_add(self):
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


    def test_order_search(self):
        api = 'customer.order.search'
        search_info = json.dumps({
            'status': 'order_launched'
        })
        self.access_api(api=api, current_page=1, search_info=search_info)


    def test_order_get(self):
        api = 'customer.order.get'
        order_id = 1
        self.access_api(api=api, order_id=order_id)
