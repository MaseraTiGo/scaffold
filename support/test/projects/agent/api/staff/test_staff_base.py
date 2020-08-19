# coding=UTF-8

import json

from support.common.testcase.agent_api_test_case import AgentAPITestCase


class StaffTestCase(AgentAPITestCase):

    def setUp(self):
        self.staff_info = {
            'name': '樱桃小丸子',
            'identification': '2131321321321321312',
            'phone': '12333333332',
            'organization_id': 1,
            'position_id': 1,
            'address': '237818280@qq.com',
            'emergency_contact': '大熊',
            'emergency_phone': '12333333331',
            'education': 'middle',
            'bank_number': '67272627627627267',
            'contract': '123213132123',
            'email': '22333333@qq.com',
            'gender': 'man',
            'diploma_img': [],
        }
        self.update_info = {
            'name': '樱桃小丸子22',
            'identification': '123321321312321312',
            'phone': '12333333344',
            'organization_id': 1,
            'position_id': 1,
            'address': '237818280@qq.com',
            'emergency_contact': '大熊2',
            'emergency_phone': '12333333331',
            'education': 'middle',
            'bank_number': '67272627627627267',
            'contract': '123213132123',
            'email': '22333333@qq.com',
            'gender': 'man',
            'diploma_img': [],
        }

    def tearDown(self):
        pass

    def assert_staff_fields(self, staff, need_id = False):
        if need_id:
            self.assertTrue('id' in staff)
        self.assertTrue('name' in staff)
        self.assertTrue('gender' in staff)
        self.assertTrue('phone' in staff)
        self.assertTrue('email' in staff)

    def test_create_staff(self):
        api = 'staff.add'
        self.access_api(
            api = api,
            staff_info = json.dumps(self.staff_info)
        )

    def test_search_staff(self):
        api = 'staff.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        for staff in result['data_list']:
            self.assert_staff_fields(staff, True)
        return result['data_list']

    def test_get_staff(self):
        staff_list = self.test_search_staff()
        staff_id = staff_list[0]['id']
        api = "staff.get"
        result = self.access_api(
            api = api,
            staff_id = staff_id
        )
        self.assertTrue('staff_info' in result)
        self.assert_staff_fields(result['staff_info'])

    def test_update_staff(self):
        staff_list = self.test_search_staff()
        staff_id = staff_list[0]['id']
        api = "staff.update"
        self.access_api(
            api = api,
            staff_id = staff_id,
            staff_info = json.dumps(self.update_info)
        )