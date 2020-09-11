# coding=UTF-8

import json

from support.common.testcase.agent_api_test_case import AgentAPITestCase
from abs.middleware.image import image_middleware
from abs.middleware.image.process import image_process

class ContractTestCase(AgentAPITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assert_contract_fields(self, contract, need_id = False):
        if need_id:
            self.assertTrue('id' in contract)
        self.assertTrue('name' in contract)
        self.assertTrue('phone' in contract)
        self.assertTrue('email' in contract)
        self.assertTrue('identification' in contract)
        self.assertTrue('create_time' in contract)

    def test_add_contract(self):
        result = image_process.get_remote_pic_size("http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/goods/8520_1599789122.jpeg")
        print("==>>>result", result, type(result))
        return
        api = 'order.contract.add'
        order_item_id = 1
        template_id = 73
        contract_info_list = json.dumps([
            {"template_param_id":54, "value":"sn_2000222"},
            {"template_param_id":55, "value":"必圈技术湖北有限公司"},
            {"template_param_id":56, "value":"张三"},
            {"template_param_id":57, "value":"123178979889080972389"},
            {"template_param_id":58, "value":"成教"},
            {"template_param_id":59, "value":"专升本"},
            {"template_param_id":60, "value":"武汉科技大学"},
            {"template_param_id":61, "value":"计算机"},
            {"template_param_id":62, "value":"10.00"},
            {"template_param_id":63, "value":"10.00"},
            {"template_param_id":64, "value":"张三"},
            {"template_param_id":65, "value":"李四"},
            {"template_param_id":66, "value":"张三"},
            {"template_param_id":67, "value":"2020.09.10"},
            {"template_param_id":68, "value":"李四"},
            {"template_param_id":69, "value":"李四"},
            {"template_param_id":70, "value":"13898989898"},
            {"template_param_id":71, "value":"2020.09.10"},
            {"template_param_id":72, "value":"http://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/goods/6298_1599731269.png"},
        ])
        result = self.access_api(
            api = api,
            order_item_id = order_item_id,
            template_id = template_id,
            contract_info_list = contract_info_list
        )
    '''
    def test_search_contract(self):
        api = 'order.contract.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)

        for contract in result['data_list']:
            self.assert_contract_fields(contract, True)
        return result['data_list']

    def test_send_contract(self):
        contract_list = self.test_search_contract()
        api = 'order.contract.send'
        contract_id = contract_list[0]["id"]
        result = self.access_api(
            api = api,
            contract_id = contract_id,
        )
    '''

