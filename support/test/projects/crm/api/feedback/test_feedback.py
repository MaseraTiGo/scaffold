# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class ToolNoticeTestCase(CrmAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_notice_search(self):
        api = 'feedback.search'
        current_page = 1
        search_info = {}
        result = self.access_api(
            api=api,
            current_page=current_page,
            search_info=json.dumps(search_info)
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        if result['data_list']:
            self.assertTrue("describe" in result['data_list'][0].keys())
        print(result['data_list'])

    def test_feedback_update_status(self):
        api = 'feedback.updatestatus'
        feedback_id = 1
        status = 'resolved'

        self.access_api(
            api=api,
            feedback_id=feedback_id,
            status=status
        )
