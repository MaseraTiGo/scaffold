# coding=UTF-8

import json

from support.common.testcase.agent_api_test_case import AgentAPITestCase


class OrderTestCase(AgentAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_order_fields(self, order, need_id = False):
        if need_id:
            self.assertTrue('id' in order)
        self.assertTrue('number' in order)
        self.assertTrue('source' in order)
        self.assertTrue('create_time' in order)
        self.assertTrue('strike_price' in order)
        self.assertTrue('actual_amount' in order)
        self.assertTrue('status' in order)
        self.assertTrue('nick' in order)
        self.assertTrue('phone' in order)
        self.assertTrue('snapshoot_list' in order)


    def test_search_order(self):
        api = 'order.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)

        for order in result['data_list']:
            self.assert_order_fields(order, True)
        return result['data_list']

    def test_get_order(self):
        order_list = self.test_search_order()
        if len(order_list) > 0:
            order_id = order_list[0]['id']
            api = "order.get"
            result = self.access_api(
                api = api,
                order_id = order_id
            )
            self.assertTrue('order_info' in result)
            self.assert_order_fields(result['order_info'])

