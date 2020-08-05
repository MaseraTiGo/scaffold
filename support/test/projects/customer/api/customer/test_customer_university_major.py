# coding=UTF-8
import json
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerUniversityMajorTest(CustomerAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_goods_search(self):
        api = 'university.major.all'
        params = {
            "current_page": 1,
            'search_info': json.dumps({})
        }
        result = self.access_api(api=api, is_auth=False, **params)
        self.assertTrue("data_list" in result)
