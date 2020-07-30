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
        self.access_api(api=api, **params)

    def test_product_goods_get(self):
        api = 'production.goods.get'
        params = {
            'goods_id': 1
        }
        self.access_api(api=api, **params)
