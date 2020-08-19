# coding=UTF-8

import json
import random
from support.common.testcase.agent_api_test_case import AgentAPITestCase
from support.common.generator.field.model.entity import YearsEntity, \
     ProductionEntity

class GoodsTestCase(AgentAPITestCase):

    def setUp(self):
        self.years = YearsEntity().generate()
        self.production = ProductionEntity().generate()
        self.goods_info = {
            'title': '计算机学与技术' + str(random.randint(0, 100)),
            'video_display': '',
            'slideshow':json.dumps([]),
            'detail':json.dumps([]),
            'market_price':10000,
            'despatch_type':"eduction_contract",
            'production_id':self.production.id if self.production else 0,
            "remark":"这事一个测试商品",
            "description":"这事一个测试商品描述",
            "years_id":self.years.id
        }
        self.update_info = {
            'title': '计算机学与技术a' + str(random.randint(0, 100)),
            'video_display': '',
            'slideshow':json.dumps([]),
            'detail':json.dumps([]),
            'market_price':10000,
            'despatch_type':"eduction_contract",
            "remark":"这事一个测试商品22",
            "description":"这事一个测试商品描述22",
            "years_id":self.years.id,
        }

    def tearDown(self):
        pass

    def assert_goods_fields(self, goods, need_id = False):
        if need_id:
            self.assertTrue('id' in goods)
        self.assertTrue('title' in goods)
        self.assertTrue('slideshow' in goods)
        self.assertTrue('production_name' in goods)
        self.assertTrue('school_name' in goods)
        self.assertTrue('major_name' in goods)
        self.assertTrue('duration' in goods)
        self.assertTrue('category' in goods)
        self.assertTrue('specification_list' in goods)

    def test_create_goods(self):
        api = 'goods.add'
        self.access_api(
            api = api,
            goods_info = json.dumps(self.goods_info)
        )

    def test_search_goods(self):
        api = 'goods.search'
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
            self.test_create_goods()
            result = self.access_api(
                api = api,
                current_page = current_page,
                search_info = json.dumps({})
            )

        for goods in result['data_list']:
            self.assert_goods_fields(goods, True)
        return result['data_list']

    def test_get_goods(self):
        goods_list = self.test_search_goods()
        goods_id = goods_list[0]['id']
        api = "goods.get"
        result = self.access_api(
            api = api,
            goods_id = goods_id
        )
        self.assertTrue('goods_info' in result)
        self.assert_goods_fields(result['goods_info'])


    def test_update_goods(self):
        goods_list = self.test_search_goods()
        goods_id = goods_list[0]['id']
        api = "goods.update"
        self.access_api(
            api = api,
            goods_id = goods_id,
            goods_info = json.dumps(self.update_info)
        )

    def test_searchall_goods(self):
        api = 'goods.searchall'
        result = self.access_api(
            api = api,
        )
        self.assertTrue("data_list" in result)

    '''
    def test_setuse_goods(self):
        goods_list = self.test_search_goods()
        goods_id = goods_list[0]['id']
        api = 'goods.setuse'
        result = self.access_api(
            api = api,
            goods_id = goods_id
        )

    def test_share_goods(self):
        goods_list = self.test_search_goods()
        goods_id = goods_list[0]['id']
        api = 'goods.share'
        result = self.access_api(
            api = api,
            goods_id = goods_id
        )
    '''
    def test_remove_goods(self):
        goods_list = self.test_search_goods()
        goods_id = goods_list[0]['id']
        api = 'goods.remove'
        result = self.access_api(
            api = api,
            goods_id = goods_id
        )
