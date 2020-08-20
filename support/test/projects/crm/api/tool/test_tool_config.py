# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class ToolConfigTestCase(CrmAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_config_fields(self, config, need_id = False):
        if need_id:
            self.assertTrue('id' in config)
        self.assertTrue('type_desc' in config)
        self.assertTrue('type' in config)
        self.assertTrue('data' in config)


    def test_search_config(self):
        api = 'tool.config.search'
        current_page = 1
        result = self.access_api(
            api = api,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        if len(result['data_list']):
            for config in result['data_list']:
                self.assert_config_fields(config)
        return result['data_list']
