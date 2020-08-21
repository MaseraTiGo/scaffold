# coding=UTF-8

import json
import random
from support.common.testcase.agent_api_test_case import AgentAPITestCase

class PosterTestCase(AgentAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_poster(self):
        api = 'goods.poster.add'
        result = self.access_api(
            api=api,
            poster_info=json.dumps({
                'sale_chance_id': 1,
                'goods_id': 1,
                'remark': '',
                'specification_list': [
                    {
                        'id': 1,
                        'sale_price': 100
                    },
                    {
                        'id': 2,
                        'sale_price': 200
                    }
                ]
            })
        )
        self.assertTrue("poster_id" in result)
