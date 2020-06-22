# coding=UTF-8

import os
import json

from support.common.testcase.api_test_case import APITestCase

class StaffTestCase(APITestCase):

    def setUp(self):
        self.staff_info = {
            'name': '杨荣凯',
            'birthday': '1990-07-07',
            'phone': '15527703115',
            'email': '237818280@qq.com',
            'gender': 'man',
            'identification': '152127198907070012',
            'entiry_time': '2020-05-02',
            'education': '2020-05-02',
        }
        self.update_info = {
            'name': '王海东',
            'id_number': 'Bq0001',
            'birthday': '1989-07-07',
            'phone': '15527703110',
            'email': '212838281@qq.com',
            'gender': 'woman',
            'identification': '15212719890707001X',
            'entiry_time': '2020-06-02',
            'education': '2012-07-01',
            'is_admin': False,
        }

    def tearDown(self):
        pass


    def assert_staff_fields(self, staff, need_id = False):
        if need_id:
            self.assertTrue('id' in staff)
        self.assertTrue('name' in staff)
        self.assertTrue('identification' in staff)
        self.assertTrue('gender' in staff)
        self.assertTrue('birthday' in staff)
        self.assertTrue('phone' in staff)
        self.assertTrue('email' in staff)
        self.assertTrue('id_number' in staff)
        self.assertTrue('is_admin' in staff)
        self.assertTrue('department_role_list' in staff)
        dr_list = staff['department_role_list']
        for dr in dr_list:
            self.assertTrue('department_role_id' in dr)
            self.assertTrue('department_id' in dr)
            self.assertTrue('department_name' in dr)
            self.assertTrue('role_id' in dr)
            self.assertTrue('role_name' in dr)


    def test_create_staff(self):
        api = 'staff.add'
        self.access_crm_api(api = api, is_auth = False, staff_info = json.dumps(self.staff_info))

    def test_search_staff(self):
        api = 'staff.search' 
        current_page = 1
        result = self.access_crm_api(api = api, current_page = current_page, search_info = json.dumps({}))
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        for staff in result['data_list']:
            self.assert_staff_fields(staff, True)
        return result['data_list']

    def test_get_staff(self):
        staff_list = self.test_search_staff()
        if staff_list:
            staff_id = staff_list[-1]['id']
            api = "staff.get"
            result = self.access_crm_api(api = api, staff_id = staff_id)
            self.assertTrue('staff_info' in result)
            self.assert_staff_fields(result['staff_info'])
        else:
            self.assertTrue("the staff_id cann't acquired! " == "")

    def test_update_staff(self):
        staff_list = self.test_search_staff()
        if staff_list:
            staff_id = staff_list[-1]['id']
            api = "staff.update"
            self.access_crm_api(api = api, staff_id = staff_id, staff_info =
                                         json.dumps(self.update_info))
        else:
            self.assertTrue("the staff_id cann't acquired! " == "")
