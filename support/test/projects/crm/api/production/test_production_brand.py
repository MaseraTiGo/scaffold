# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class ProductionBrandTestCase(CrmAPITestCase):

    def setUp(self):
        self.brand_info = {
            'name': '教育',
            'industry': 'education',
            'description': '教育行业',
        }
        self.update_info = {
            'name': '电商',
            'industry': 'e-commerce',
            'description': '电商行业',
        }

    def tearDown(self):
        pass

    def assert_brand_fields(self, brand, need_id=False):
        if need_id:
            self.assertTrue('id' in brand)
        self.assertTrue('name' in brand)
        self.assertTrue('industry' in brand)
        self.assertTrue('description' in brand)
        self.assertTrue('company_id' in brand)
        self.assertTrue('create_time' in brand)

    def test_create_brand(self):
        api = 'production.brand.add'
        self.access_api(
            api=api,
            brand_info=json.dumps(self.brand_info)
        )

    def test_search_brand(self):
        api = 'production.brand.search'
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
            self.test_create_brand()
            result = self.access_api(
                api=api,
                current_page=current_page,
                search_info=json.dumps({})
            )

        for brand in result['data_list']:
            self.assert_brand_fields(brand, True)
        return result['data_list']

    def test_search_all_brand(self):
        api = 'production.brand.searchall'
        result = self.access_api(
            api=api,
        )
        self.assertTrue("data_list" in result)
        if not len(result['data_list']):
            self.test_create_brand()
            result = self.access_api(
                api=api,
            )

        for brand in result['data_list']:
            self.assert_brand_fields(brand, True)
        return result['data_list']

    def test_get_brand(self):
        brand_list = self.test_search_brand()
        brand_id = brand_list[-1]['id']
        api = "production.brand.get"
        result = self.access_api(
            api=api,
            brand_id=brand_id
        )
        self.assertTrue('brand_info' in result)
        self.assert_brand_fields(result['brand_info'])

    def test_update_brand(self):
        brand_list = self.test_search_brand()
        brand_id = brand_list[-1]['id']
        api = "production.brand.update"
        self.access_api(
            api=api,
            brand_id=brand_id,
            update_info=json.dumps(self.update_info)
        )

    def test_remove_brand(self):
        brand_list = self.test_search_brand()
        brand_id = brand_list[0]['id']
        api = 'production.brand.remove'
        result = self.access_api(
            api=api,
            brand_id=brand_id
        )
