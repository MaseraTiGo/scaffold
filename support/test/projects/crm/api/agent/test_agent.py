# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class AgentTestCase(CrmAPITestCase):

    def setUp(self):
        self.agent_info = {
            "name":"上谷网络科技有限公司",
            "province":"湖北省",
            "city":"武汉市",
            "area":"洪山区",
            "address":"光谷大道光谷总部国际",
            "license_code":"2131jkjdfk1231kjdskf",
            "license_picture":"",
            "official_seal":""
        }
        self.update_info = {
            "name":"上谷网络科技有限公司001",
            "province":"湖北省",
            "city":"武汉市",
            "area":"洪山区",
            "address":"光谷大道光谷总部国际001",
            "license_code":"2131jkjdfk1231kjdskf",
            "license_picture":"",
            "official_seal":""
        }

    def tearDown(self):
        pass

    def assert_agent_fields(self, agent, need_id = False):
        if need_id:
            self.assertTrue('id' in agent)
        self.assertTrue('name' in agent)
        self.assertTrue('province' in agent)
        self.assertTrue('city' in agent)
        self.assertTrue('area' in agent)
        self.assertTrue('address' in agent)
        self.assertTrue('license_code' in agent)
        self.assertTrue('create_time' in agent)

    def test_create_agent(self):
        api = 'agent.add'
        self.access_api(
            api = api,
            agent_info = json.dumps(self.agent_info)
        )

    def test_search_agent(self):
        api = 'agent.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        if not len(result['data_list']):
            self.test_create_agent()
            result = self.access_api(
                api = api,
                current_page = current_page,
                search_info = json.dumps({})
            )
        for agent in result['data_list']:
            self.assert_agent_fields(agent, True)
        return result['data_list']

    def test_searchall_agent(self):
        api = 'agent.searchall'
        current_page = 1
        result = self.access_api(
            api = api,
        )
        self.assertTrue("data_list" in result)
        return result['data_list']

    def test_get_agent(self):
        agent_list = self.test_search_agent()
        agent_id = agent_list[0]['id']
        api = "agent.get"
        result = self.access_api(
            api = api,
            agent_id = agent_id
        )
        self.assertTrue('agent_info' in result)
        self.assert_agent_fields(result['agent_info'])

    def test_update_agent(self):
        agent_list = self.test_search_agent()
        agent_id = agent_list[0]['id']
        api = "agent.update"
        self.access_api(
            api = api,
            agent_id = agent_id,
            agent_info = json.dumps(self.update_info)
        )

