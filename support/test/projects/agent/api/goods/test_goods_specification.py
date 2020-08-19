# coding=UTF-8

import json
import random
from support.common.testcase.agent_api_test_case import AgentAPITestCase
from support.common.generator.field.model.entity import GoodsEntity, \
     SpecificationEntity


class GoodsSpecificationTestCase(AgentAPITestCase):

    def setUp(self):
        self.goods = GoodsEntity().generate()
        self.specification = SpecificationEntity().generate()
        self.specification_list = [{
            'show_image': '',
            'sale_price': 100,
            'stock':100,
            'specification_value_list':[{
                "category":"网络",
                "attribute":"5G"
            }]
        }]
        self.update_info = {
            'show_image': '',
            'sale_price': 200,
            'stock':200,
            'remark':''
        }

    def tearDown(self):
        pass

    def assert_sepcification_fields(self, sepcification, need_id = False):
        if need_id:
            self.assertTrue('id' in sepcification)
        self.assertTrue('show_image' in sepcification)
        self.assertTrue('sale_price' in sepcification)
        self.assertTrue('stock' in sepcification)
        self.assertTrue('remark' in sepcification)
        self.assertTrue('specification_value_list' in sepcification)


    def test_create_sepcification(self):
        api = 'goods.specification.add'
        goods_id = self.goods.id
        self.access_api(
            api = api,
            goods_id = goods_id,
            specification_list = json.dumps(self.specification_list)
        )

    def test_get_sepcification(self):
        api = "goods.specification.get"
        result = self.access_api(
            api = api,
            specification_id = self.specification.id
        )
        self.assertTrue('specification_info' in result)
        self.assert_sepcification_fields(result['specification_info'])

    def test_update_sepcification(self):
        api = "goods.specification.update"
        self.access_api(
            api = api,
            specification_id = self.specification.id,
            update_info = json.dumps(self.update_info)
        )

    def test_remove_sepcification(self):
        api = 'goods.specification.remove'
        result = self.access_api(
            api = api,
            specification_id = self.specification.id
        )
