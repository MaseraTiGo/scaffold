# coding=UTF-8

import json

from support.common.testcase.agent_api_test_case import AgentAPITestCase


class StaffTestCase(AgentAPITestCase):

    def setUp(self):
        self.staff_info = {
            'nick': '小丸子',
            'head_url': 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1990625098,3468619056&fm=11&gp=0.jpg',
            'name': '杨荣凯',
            'birthday': '1990-07-07',
            'phone': '15527703115',
            'email': '237818280@qq.com',
            'gender': 'man',
        }
        self.update_info = {
            'nick': '蜡笔小新',
            'head_url': 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2091711702,2468700162&fm=11&gp=0.jpg',
            'name': '王海东',
            'work_number': 'Bq0002',
            'birthday': '1989-07-07',
            'phone': '15527703110',
            'email': '212838281@qq.com',
            'gender': 'woman',
            'is_admin': False,
        }

    def tearDown(self):
        pass

    def assert_staff_fields(self, staff, need_id = False):
        if need_id:
            self.assertTrue('id' in staff)
        self.assertTrue('nick' in staff)
        self.assertTrue('head_url' in staff)
        self.assertTrue('name' in staff)
        self.assertTrue('gender' in staff)
        self.assertTrue('birthday' in staff)
        self.assertTrue('phone' in staff)
        self.assertTrue('email' in staff)
        self.assertTrue('work_number' in staff)
        self.assertTrue('username' in staff)
        self.assertTrue('status' in staff)
        self.assertTrue('last_login_time' in staff)
        self.assertTrue('is_admin' in staff)
        self.assertTrue('department_role_list' in staff)
        dr_list = staff['department_role_list']
        for dr in dr_list:
            self.assertTrue('department_role_id' in dr)
            self.assertTrue('department_id' in dr)
            self.assertTrue('department_name' in dr)
            self.assertTrue('role_id' in dr)
            self.assertTrue('role_name' in dr)


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

