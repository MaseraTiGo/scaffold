# coding=UTF-8

import json

from support.common.testcase.agent_api_test_case import AgentAPITestCase


class AgentNoticeTest(AgentAPITestCase):

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def test_account_register(self):
        api = 'agent.notice.search'
        params = {'current_page': 1}
        result = self.access_api(api=api, **params)
        print(f'get notice result: \n{result}')
        for item in result.get('data_list', []):
            self.assertTrue('title' in item.keys())
            self.assertTrue('content' in item.keys())
            self.assertTrue('datetime' in item.keys())