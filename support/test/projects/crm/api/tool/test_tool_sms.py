# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class ToolSmsTestCase(CrmAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_sms_fields(self, sms, need_id = False):
        if need_id:
            self.assertTrue('id' in sms)
        self.assertTrue('phone' in sms)
        self.assertTrue('content' in sms)
        self.assertTrue('scene' in sms)
        self.assertTrue('source_type' in sms)
        self.assertTrue('status' in sms)
        self.assertTrue('create_time' in sms)


    def test_search_sms(self):
        api = 'tool.sms.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        if len(result['data_list']):
            for sms in result['data_list']:
                self.assert_sms_fields(sms, True)
        return result['data_list']
