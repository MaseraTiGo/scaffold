# coding=UTF-8

import json

from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerTestCase(CustomerAPITestCase):

    def setUp(self):
        self.certification_info = {
            'name': '张杰芳',
            'identification': '422202199610021840',
            'id_front': 'http://bq-crm-resouce.oss-cn-beijing.aliyuncs.com/pos-install%2Fimage%2F202007%2F13184325740513.jpg',
            'id_back': 'http://bq-crm-resouce.oss-cn-beijing.aliyuncs.com/pos-install%2Fimage%2F202007%2F13184325740513.jpg',
            'id_in_hand': 'http://bq-crm-resouce.oss-cn-beijing.aliyuncs.com/pos-install%2Fimage%2F202007%2F13184325740513.jpg'
        }

    def tearDown(self):
        pass

    def assert_certification_fields(self, certification):
        self.assertTrue('name' in certification)
        self.assertTrue('identification' in certification)
        self.assertTrue('id_front' in certification)
        self.assertTrue('id_back' in certification)
        self.assertTrue('id_in_hand' in certification)

    def test_customer_myself_authenticate(self):
        api = 'customer.myself.real.authenticate'
        self.access_api(
            api,
            certification_info=json.dumps(self.certification_info)
        )

    def test_customer_myself_get(self):
        api = 'customer.myself.real.get'
        result = self.access_api(
            api
        )
        self.assertTrue("certification_info" in result)
        self.assert_certification_fields(result['certification_info'])
