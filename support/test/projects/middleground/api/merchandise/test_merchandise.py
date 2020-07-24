# coding=UTF-8

import json

from support.common.testcase.middleground_api_test_case import \
        MiddlegroundAPITestCase
from support.common.generator.field.model.entity import ProductionEntity,\
        SpecificationEntity


class MerchandiseTestCase(MiddlegroundAPITestCase):

    def setUp(self):
        self.production = ProductionEntity().generate()
        self.company_id = self.production.company_id
        self.merchandise_info = {
            'title': self.production.name + '商品',
            'video_display': 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2091711702,2468700162&fm=11&gp=0.jpg',
            'slideshow': [
                "https://www.baidu.com",
                "https://www.baidu.com",
                "https://www.baidu.com",
                "https://www.baidu.com",
                "https://www.baidu.com",
            ],
            'detail': [
                "https://baidu.com",
                "https://baidu.com",
                "https://baidu.com",
                "https://baidu.com",
                "https://baidu.com",
            ],
            'pay_types': [
                "bank",
                "alipay",
                "wechat",
            ],
            'pay_services': [
                "full_payment",
                "installment",
            ],
            'market_price': 10000,
            'despatch_type': 'logistics',
            'company_id': self.company_id,
            'production_id': self.production.id,
            'remark': '测试',
        }
        self.update_info = {
            'title': self.production.name + '商品-修改',
            'video_display': 'https://www.baidu.com',
            'slideshow': [
                "https://www.baidu.com",
                "https://www.baidu.com",
            ],
            'detail': [
                "https://baidu.com",
            ],
            'pay_types': [
                "alipay",
                "wechat",
            ],
            'pay_services': [
                "installment",
            ],
            'market_price': 20000,
            'despatch_type': 'logistics',
            'company_id': self.company_id,
            'production_id': self.production.id,
            'remark': '测试',
            'use_status': 'enable',
        }

        self.specification_info = {
            'show_image': "https://wwww.baidu.com",
            'sale_price': 15000,
            'stock': 150,
            'remark': "临时产品",
            'attribute_list': [
                {
                    'category': "课程",
                    'attribute': "vip",
                }
            ],
        }
        self.specification_update_info = {
            'show_image': "https://wwww.xinlang.com",
            'sale_price': 18000,
            'stock': 180,
            'remark': "临时产品",
            'attribute_list': [
                {
                    'category': "课程",
                    'attribute': "vip",
                }
            ],
        }

    def tearDown(self):
        pass

    def assert_merchandise_specifaction_fields(self, specification, need_id=False):
        self.assertTrue('id' in specification)
        self.assertTrue('sale_price' in specification)
        self.assertTrue('show_image' in specification)
        self.assertTrue('stock' in specification)
        self.assertTrue('remark' in specification)
        self.assertTrue('specification_value_list' in specification)
        specification_value_list = specification['specification_value_list']
        for specification_value in specification_value_list:
            self.assertTrue('category' in specification_value)
            self.assertTrue('attribute' in specification_value)

    def assert_merchandise_fields(self, merchandise, need_id=False):
        if need_id:
            self.assertTrue('id' in merchandise)
        self.assertTrue('title' in merchandise)
        self.assertTrue('video_display' in merchandise)
        self.assertTrue('slideshow' in merchandise)
        self.assertTrue('detail' in merchandise)
        self.assertTrue('pay_types' in merchandise)
        self.assertTrue('pay_services' in merchandise)
        self.assertTrue('market_price' in merchandise)
        self.assertTrue('despatch_type' in merchandise)
        self.assertTrue('company_id' in merchandise)
        self.assertTrue('production_id' in merchandise)
        self.assertTrue('use_status' in merchandise)
        self.assertTrue('remark' in merchandise)
        self.assertTrue('specification_list' in merchandise)
        specification_list = merchandise['specification_list']
        for specification in specification_list:
            self.assert_merchandise_specifaction_fields(specification)

    def test_create_merchandise(self):
        api = 'merchandise.add'
        result = self.access_api(
            api=api,
            merchandise_info=json.dumps(self.merchandise_info)
        )
        self.assertTrue('merchandise_id' in result)

    def test_search_merchandise(self):
        api = 'merchandise.search'
        current_page = 1
        result = self.access_api(
            api=api,
            company_id=self.company_id,
            current_page=current_page,
            search_info=json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        merchandise_list = result['data_list']
        if len(merchandise_list) == 0:
            self.test_create_merchandise()
            result = self.access_api(
                api=api,
                copany_id=self.company_id,
                current_page=current_page,
                search_info=json.dumps({})
            )

        for merchandise in result['data_list']:
            self.assert_merchandise_fields(merchandise, True)
        return result['data_list']

    def test_get_merchandise(self):
        merchandise_list = self.test_search_merchandise()
        merchandise_id = merchandise_list[-1]['id']
        api = "merchandise.get"
        result = self.access_api(
            api=api,
            merchandise_id=merchandise_id
        )
        self.assertTrue('merchandise_info' in result)
        self.assert_merchandise_fields(result['merchandise_info'])

    def test_update_merchandise(self):
        merchandise_list = self.test_search_merchandise()
        merchandise_id = merchandise_list[-1]['id']
        api = "merchandise.update"
        self.access_api(
            api=api,
            merchandise_id=merchandise_id,
            update_info=json.dumps(self.update_info)
        )

    def test_get_specification_specification(self):
        self.test_add_specification_specification()
        specification_id = SpecificationEntity().generate().id
        api = "merchandise.specification.get"
        self.access_api(
            api=api,
            specification_id=specification_id,
            update_info=json.dumps(self.update_info)
        )

    def test_add_specification_specification(self):
        merchandise_id = self.test_search_merchandise()[-1]['id']
        api = "merchandise.specification.add"
        result = self.access_api(
            api=api,
            merchandise_id=merchandise_id,
            specification_info=json.dumps(self.specification_info)
        )
        self.assertTrue('specification_id' in result)
        return result['specification_id']

    def test_update_specification_specification(self):
        self.test_add_specification_specification()
        specification_id = SpecificationEntity().generate().id
        api = "merchandise.specification.update"
        self.access_api(
            api=api,
            specification_id=specification_id,
            update_info=json.dumps(self.specification_update_info)
        )

    def test_remove_specification_specification(self):
        self.test_add_specification_specification()
        specification_id = SpecificationEntity().generate().id
        api = "merchandise.specification.remove"
        self.access_api(
            api=api,
            specification_id=specification_id,
        )
