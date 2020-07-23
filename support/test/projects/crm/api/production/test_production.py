# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase
from support.common.generator.field.model.entity import BrandEntity


class ProductionproductionTestCase(CrmAPITestCase):

    def setUp(self):
        self._brand = BrandEntity().generate()
        self.production_info = {
            'name': '专升本',
            'description': '专科升级到本科',
            'attribute_list': [
                {
                    'category': "课程",
                    "attribute_list": [
                        {
                            "name": "vip课程",
                        },
                        {
                            "name": "普通课程",
                        },
                        {
                            "name": "视频课程",
                        },
                    ]
                },
                {
                    'category': "支付方式",
                    "attribute_list": [
                        {
                            "name": "一次性付清",
                        },
                        {
                            "name": "分期付款",
                        },
                    ]
                },
            ],
            'workflow_list': [
                {
                    'name': "专科报名",
                    'type': "report",
                    'description': "学员升学需要进行全国统一报名考试",
                },
                {
                    'name': "科一考试",
                    'type': "test",
                    'description': "学员第一课考试进行",
                },
                {
                    'name': "科二考试",
                    'type': "test",
                    'description': "学员第二课考试进行",
                },
                {
                    'name': "科三考试",
                    'type': "test",
                    'description': "学员第三课考试进行",
                },
                {
                    'name': "领取毕业证",
                    'type': "graduation",
                    'description': "学员毕业",
                },
            ],
        }
        self.update_info = {
            'name': '高升本',
            'description': '高中升级到本科',
            'attribute_list': [
                {
                    'category': "课程",
                    "attribute_list": [
                        {
                            "name": "vip课程",
                        },
                        {
                            "name": "普通课程",
                        },
                        {
                            "name": "视频课程",
                        },
                    ]
                },
                {
                    'category': "支付方式",
                    "attribute_list": [
                        {
                            "name": "一次性付清",
                        },
                        {
                            "name": "分期付款",
                        },
                    ]
                },
            ],
            'workflow_list': [
                {
                    'name': "专科报名",
                    'type': "report",
                    'description': "学员升学需要进行全国统一报名考试",
                },
                {
                    'name': "科一考试",
                    'type': "test",
                    'description': "学员第一课考试进行",
                },
                {
                    'name': "科二考试",
                    'type': "test",
                    'description': "学员第二课考试进行",
                },
                {
                    'name': "领取毕业证",
                    'type': "graduation",
                    'description': "学员毕业",
                },
            ],
        }

    def tearDown(self):
        pass

    def assert_production_fields(self, production, need_id=False):
        if need_id:
            self.assertTrue('id' in production)
        self.assertTrue('name' in production)
        self.assertTrue('description' in production)
        self.assertTrue('attribute_list' in production)
        self.assertTrue('workflow_list' in production)
        self.assertTrue('brand_id' in production)
        self.assertTrue('brand_name' in production)
        self.assertTrue('update_time' in production)
        self.assertTrue('create_time' in production)

    def test_create_production(self):
        api = 'production.add'
        self.access_api(
            api=api,
            brand_id=self._brand.id,
            production_info=json.dumps(self.production_info)
        )

    def test_search_production(self):
        api = 'production.search'
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
            self.test_create_production()
            result = self.access_api(
                api=api,
                current_page=current_page,
                search_info=json.dumps({})
            )

        for production in result['data_list']:
            self.assert_production_fields(production, True)
        return result['data_list']

    def test_get_production(self):
        production_list = self.test_search_production()
        production_id = production_list[-1]['id']
        api = "production.get"
        result = self.access_api(
            api=api,
            production_id=production_id
        )
        self.assertTrue('production_info' in result)
        self.assert_production_fields(result['production_info'])

    def test_update_production(self):
        production_list = self.test_search_production()
        production_id = production_list[-1]['id']
        api = "production.update"
        self.access_api(
            api=api,
            production_id=production_id,
            update_info=json.dumps(self.update_info)
        )
