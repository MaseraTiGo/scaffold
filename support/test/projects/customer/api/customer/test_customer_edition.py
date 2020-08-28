# coding=UTF-8
import json
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerEditionTest(CustomerAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_edition_get(self):
        api = 'edition.get'
        type = 'ios'
        result = self.access_api(api = api, type = type)
        print("===>>>result)", result["edition_info"])
        self.assertTrue("edition_info" in result)
