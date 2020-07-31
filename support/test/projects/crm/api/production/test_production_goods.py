# coding=UTF-8

import json
import random
from support.common.testcase.crm_api_test_case import CrmAPITestCase
from support.common.generator.field.model.entity import SchoolEntity, \
     MajorEntity, ProductionEntity

class ProductionGoodsTestCase(CrmAPITestCase):

    def setUp(self):
        self.school = SchoolEntity().generate()
        self.major = SchoolEntity().generate()
        self.production = ProductionEntity().generate()
        self.goods_info = {
            'title': '计算机学与技术' + str(random.randint(0, 100)),
            'video_display': '/1231/123.mp3',
            'slideshow':json.dumps(["/1231/1.png"]),
            'detail':json.dumps(["/1231/1.png"]),
            'market_price':10000,
            'despatch_type':"eduction_contract",
            'production_id':self.production.id if self.production else 0,
            'school_id':self.school.id if self.school else 0,
            'major_id':self.major.id if self.major else 0,
            "duration":"two_half_year",
            "remark":"这事一个测试商品",
            "description":"这事一个测试商品描述",
            "specification_list":[{
              "show_image":"/1231/1.png",
              "sale_price":10200,
              "stock":30,
              "specification_value_list":[{
                 "category":"颜色",
                 "attribute":"白色"
               },
               {
                 "category":"尺寸",
                 "attribute":"L"
               }]
            }]
        }
        self.update_info = {
            'title': '计算机学与技术a' + str(random.randint(0, 100)),
            'video_display': '/1231/123.mp3',
            'slideshow':json.dumps(["/1231/1.png"]),
            'detail':json.dumps(["/1231/1.png"]),
            'market_price':10000,
            'despatch_type':"eduction_contract",
            'production_id':self.production.id if self.production else 0,
            'school_id':self.school.id if self.school else 0,
            'major_id':self.major.id if self.major else 0,
            "duration":"one_half_year",
            "remark":"这事一个测试商品22",
            "description":"这事一个测试商品描述22",
            "use_status":"enable",
            "specification_list":[{
              "show_image":"/1231/1.png",
              "sale_price":10200,
              "stock":40,
              "specification_value_list":[{
                 "category":"颜色2",
                 "attribute":"白色2"
               },
               {
                 "category":"尺寸2",
                 "attribute":"ML"
               }]
            }]
        }

    def tearDown(self):
        pass

    def assert_goods_fields(self, goods, need_id=False):
        if need_id:
            self.assertTrue('id' in goods)
        self.assertTrue('title' in goods)
        self.assertTrue('slideshow' in goods)
        self.assertTrue('production_name' in goods)
        self.assertTrue('school_name' in goods)
        self.assertTrue('major_name' in goods)
        self.assertTrue('duration' in goods)
        self.assertTrue('specification_list' in goods)

    def test_create_goods(self):
        api = 'production.goods.add'
        self.access_api(
            api=api,
            goods_info=json.dumps(self.goods_info)
        )

    def test_search_goods(self):
        api = 'production.goods.search'
        current_page = 1
        result = self.access_api(
            api=api,
            current_page=current_page,
            search_info=json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        if not len(result['data_list']):
            self.test_create_goods()
            result = self.access_api(
                api=api,
                current_page=current_page,
                search_info=json.dumps({})
            )

        for goods in result['data_list']:
            self.assert_goods_fields(goods, True)
        return result['data_list']

    def test_get_goods(self):
        goods_list = self.test_search_goods()
        goods_id = goods_list[0]['id']
        api = "production.goods.get"
        result = self.access_api(
            api=api,
            goods_id=goods_id
        )
        self.assertTrue('goods_info' in result)
        self.assert_goods_fields(result['goods_info'])


    def test_update_goods(self):
        goods_list = self.test_search_goods()
        goods_id = goods_list[0]['id']
        specification_id = goods_list[0]["specification_list"][0]["id"]
        api = "production.goods.update"
        self.update_info["specification_list"][0]["id"] = specification_id
        self.access_api(
            api=api,
            goods_id=goods_id,
            goods_info=json.dumps(self.update_info)
        )

    def test_setuse_goods(self):
        goods_list = self.test_search_goods()
        goods_id = goods_list[0]['id']
        api = 'production.goods.setuse'
        result = self.access_api(
            api=api,
            goods_id=goods_id
        )

    def test_remove_goods(self):
        goods_list = self.test_search_goods()
        goods_id = goods_list[0]['id']
        api = 'production.goods.remove'
        result = self.access_api(
            api=api,
            goods_id=goods_id
        )
