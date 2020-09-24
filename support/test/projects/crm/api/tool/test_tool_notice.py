# coding=UTF-8

import json
from random import choice
from support.common.testcase.crm_api_test_case import CrmAPITestCase


class ToolNoticeTestCase(CrmAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_random_data(self, data_list, only_id=True):
        if not data_list:
            return None
        return choice(data_list) if not only_id else choice(data_list)['id']

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
            for notice in result['data_list']:
                self.assertTrue('content' in notice.keys())
        # print(result['data_list'])
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
        data_list = self.test_notice_search()
        notice_id = self.get_random_data(data_list)
        if not notice_id:
            print(f'no data 2 delete')
            return
        result = self.access_api(
            api=api,
            notice_id=notice_id
        )
        # self.assertTrue(result, True)

    def test_notice_update(self):
        api = 'tool.notice.update'
        data_list = self.test_notice_search()
        notice_id = self.get_random_data(data_list)
        if not notice_id:
            print(f'no data 4 updating')
            return
        update_info = {
            'content': 'this content has been modified!'
        }
        result = self.access_api(
            api=api,
            notice_id=notice_id,
            update_info=json.dumps(update_info)
        )

    def test_notice_search_all(self):
        api = 'tool.notice.searchall'
        result = self.access_api(
            api=api
        )
        self.assertTrue("data_list" in result)
        if len(result['data_list']):
            for notice in result['data_list']:
                self.assertTrue(notice.get('status') == 'enable')
        print(result['data_list'])
