# coding=UTF-8

import json

from support.common.testcase.agent_api_test_case import AgentAPITestCase


class CustomerTestCase(AgentAPITestCase):

    def setUp(self):
        self.update_info = {
            "name":"张三012",
            "city":"辽宁省-抚顺市-新抚区",
            "education":"high"
        }

    def tearDown(self):
        pass

    def assert_customer_fields(self, customer, need_id = False):
        if need_id:
            self.assertTrue('id' in customer)
        self.assertTrue('nick' in customer)
        self.assertTrue('head_url' in customer)
        self.assertTrue('name' in customer)
        self.assertTrue('gender' in customer)
        self.assertTrue('birthday' in customer)
        self.assertTrue('phone' in customer)
        self.assertTrue('email' in customer)
        self.assertTrue('wechat' in customer)
        self.assertTrue('qq' in customer)
        self.assertTrue('create_time' in customer)

    def test_search_customer(self):
        api = 'customer.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)

        for customer in result['data_list']:
            self.assert_customer_fields(customer, True)
        return result['data_list']

    def test_update_customer(self):
        customer_list = self.test_search_customer()
        api = 'customer.update'
        agent_customer_id = customer_list[0]['id']
        result = self.access_api(
            api = api,
            agent_customer_id = agent_customer_id,
            update_info = json.dumps(
                self.update_info
            )
        )

