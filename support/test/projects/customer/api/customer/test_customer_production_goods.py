# coding=UTF-8
import json
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerProductionGoodsTest(CustomerAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_account_phone_verification_code(self):
        api = 'customer.production.goods.search'
        params = {
            "current_page": 1,
            'search_info': json.dumps({})
        }
        self.access_api(api=api, is_auth=False, **params)
