# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class StaffTestCase(CrmAPITestCase):

    def setUp(self):
        self.staff_info = {
            'name': '宁缺',
            'birthday': '1990-07-07',
            'phone': '15527703111',
            'email': '237818280@qq.com',
            'gender': 'man',
        }
        self.update_info = {
            'name': '宁缺22',
            'birthday': '1990-07-07',
            'phone': '15527703111',
            'email': '237818280@qq.com',
            'gender': 'man',
        }

    def tearDown(self):
        pass

    def assert_staff_fields(self, staff, need_id = False):
        if need_id:
            self.assertTrue('id' in staff)
        self.assertTrue('name' in staff)
        self.assertTrue('gender' in staff)
        self.assertTrue('birthday' in staff)
        self.assertTrue('phone' in staff)
        self.assertTrue('email' in staff)
        self.assertTrue('work_number' in staff)
        self.assertTrue('is_admin' in staff)

    def test_create_staff(self):
        api = 'staff.add'
        self.access_api(api = api, staff_info = json.dumps(self.staff_info))

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

        if result['total'] <= 0:
            self.test_create_staff()
            result = self.access_api(
                api = api,
                current_page = current_page,
                search_info = json.dumps({})
            )

        for staff in result['data_list']:
            self.assert_staff_fields(staff, True)
        return result['data_list']

    def test_get_staff(self):
        staff_list = self.test_search_staff()
        staff_id = staff_list[0]['id']
        api = "staff.get"
        result = self.access_api(api = api, staff_id = staff_id)
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
