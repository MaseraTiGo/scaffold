# coding=UTF-8

import json

from support.common.testcase.agent_api_test_case import AgentAPITestCase
from support.common.generator.field.model.entity import ProductionEntity


class CustomerChanceTestCase(AgentAPITestCase):

    def setUp(self):
        self.production = ProductionEntity().generate()
        self.sale_chance_info = {
            'name': '张三丰',
            'phone': '13223090000',
            'production_id': self.production.id,
            'city':"湖北省武汉市洪山区",
            'education':"middle",
            'remark':'123131',
        }

    def tearDown(self):
        pass

    def assert_chance_fields(self, chance, need_id = False):
        if need_id:
            self.assertTrue('id' in chance)
        self.assertTrue('phone' in chance)
        self.assertTrue('name' in chance)
        self.assertTrue('wechat' in chance)
        self.assertTrue('education' in chance)
        self.assertTrue('production_id' in chance)
        self.assertTrue('production_name' in chance)
        self.assertTrue('city' in chance)
        self.assertTrue('staff_id' in chance)
        self.assertTrue('staff_name' in chance)
        self.assertTrue('remark' in chance)
        self.assertTrue('end_time' in chance)
        self.assertTrue('create_time' in chance)

    '''
    def test_create_chance(self):
        api = 'customer.salechance.add'
        self.access_api(
            api = api,
            sale_chance_info = json.dumps(self.sale_chance_info)
        )
    '''
    def test_search_customer(self):
        api = 'customer.salechance.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        for chance in result['data_list']:
            self.assert_chance_fields(chance, True)
        return result['data_list']
