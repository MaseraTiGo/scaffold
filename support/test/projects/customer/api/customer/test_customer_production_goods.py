# coding=UTF-8
import json
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerProductionGoodsTest(CustomerAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_goods_search(self):
        api = 'production.goods.search'
        params = {
            "current_page": 1,
            'search_info': json.dumps({})
        }
        result = self.access_api(api=api, is_auth=False, **params)
        self.assertTrue("data_list" in result)

    def test_product_goods_get(self):
        api = 'production.goods.get'
        params = {
            'goods_id': 1
        }
        result = self.access_api(api=api, is_auth=False, **params)
        self.assertTrue("goods_info" in result)

    def test_product_goods_hotsearch(self):
        api = 'production.goods.hotsearch'
        params = {
            "current_page": 1,
            'search_info': json.dumps({
                'city': '武汉'
            })
        }
        result = self.access_api(api=api, is_auth=False, **params)
        self.assertTrue("data_list" in result)
