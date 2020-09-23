# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class ToolNoticeTestCase(CrmAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_sms_fields(self, sms, need_id=False):
        if need_id:
            self.assertTrue('id' in sms)
        self.assertTrue('phone' in sms)
        self.assertTrue('content' in sms)
        self.assertTrue('scene' in sms)
        self.assertTrue('source_type' in sms)
        self.assertTrue('status' in sms)
        self.assertTrue('create_time' in sms)

    def test_notice_search(self):
        api = 'tool.notice.search'
        current_page = 1
        result = self.access_api(
            api=api,
            current_page=current_page,
            search_info=json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        if len(result['data_list']):
            for sms in result['data_list']:
                self.assert_sms_fields(sms, True)
        return result['data_list']

    def test_notice_add(self):
        api = 'tool.notice.add'
        notice_info = {
            'classify': 'notify',
            'content': 'this is a simple test',
            'status': 'enable',
            'platform': 'crm'
        }

        self.access_api(
            api=api,
            notice_info=json.dumps(notice_info)
        )
        # self.assertTrue(result, True)

    def test_notice_remove(self):
        api = 'tool.notice.remove'
        notice_id = 1
        result = self.access_api(
            api=api,
            notice_id=notice_id
        )
        # self.assertTrue(result, True)

    def test_notice_update(self):
        api = 'tool.notice.update'
        notice_id = 2
        update_info = {
            'content': 'this content has been modified!'
        }
        result = self.access_api(
            api=api,
            notice_id=notice_id,
            update_info=json.dumps(update_info)
        )
