# coding=UTF-8
import json
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerUniversitySchoolTest(CustomerAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_goods_all(self):
        api = 'university.school.all'
        params = {
            'search_info': json.dumps({})
        }
        result = self.access_api(api=api, **params)
        self.assertTrue("data_list" in result)

    def test_product_goods_search(self):
        api = 'university.school.search'
        params = {
            "current_page": 1,
            'search_info': json.dumps({})
        }
        result = self.access_api(api=api, **params)
        self.assertTrue("data_list" in result)

    def test_product_goods_hotsearch(self):
        api = 'university.school.hotsearch'
        params = {
            'search_info': json.dumps({})
        }
        result = self.access_api(api=api, **params)
        self.assertTrue("data_list" in result)

    def test_product_goods_get(self):
        api = 'university.school.get'
        params = {
            'school_id': 1
        }
        result = self.access_api(api=api, **params)
        self.assertTrue("school_info" in result)
