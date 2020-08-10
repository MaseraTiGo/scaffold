# coding=UTF-8

import json

from support.common.testcase.agent_api_test_case import AgentAPITestCase


class ContractTestCase(AgentAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_contract_fields(self, contract, need_id = False):
        if need_id:
            self.assertTrue('id' in contract)
        self.assertTrue('name' in contract)
        self.assertTrue('phone' in contract)
        self.assertTrue('email' in contract)
        self.assertTrue('identification' in contract)
        self.assertTrue('create_time' in contract)


    def test_search_contract(self):
        api = 'order.contract.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)

        for contract in result['data_list']:
            self.assert_contract_fields(contract, True)
        return result['data_list']
