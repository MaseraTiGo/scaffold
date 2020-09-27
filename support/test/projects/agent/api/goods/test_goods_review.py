# coding=UTF-8

import json
from random import choice
from support.common.testcase.agent_api_test_case import AgentAPITestCase


class ToolNoticeTestCase(AgentAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def get_random_data(self, data_list, only_id=True):
        if not data_list:
            return None
        return choice(data_list) if not only_id else choice(data_list)['id']

    def test_goods_review_search(self):
        api = 'goods.review.search'
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
                self.assertTrue('remark' in notice.keys())
        print(result['data_list'])
        return result['data_list']

    def test_goods_review_setstatus(self):
        api = 'goods.review.setstatus'
        goods_id = 1
        self.access_api(
            api=api,
            goods_id=goods_id
        )

