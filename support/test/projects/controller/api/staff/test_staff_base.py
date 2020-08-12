# coding=UTF-8

import json

from support.common.testcase.controller_api_test_case import \
        ControllerAPITestCase


class StaffTestCase(ControllerAPITestCase):

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

    def assert_staff_fields(self, staff, is_search=True):
        self.assertTrue('id' in staff)
        self.assertTrue('name' in staff)
        self.assertTrue('gender' in staff)
        self.assertTrue('birthday' in staff)
        self.assertTrue('phone' in staff)
        self.assertTrue('email' in staff)
        self.assertTrue('work_number' in staff)
        self.assertTrue('is_admin' in staff)
        if not is_search:
            self.assertTrue('account_info' in staff)
            account = staff['account_info']
            self.assertTrue('nick' in account)
            self.assertTrue('head_url' in account)
            self.assertTrue('last_login_time' in account)
            self.assertTrue('last_login_ip' in account)
            self.assertTrue('register_ip' in account)
            self.assertTrue('status' in account)
            self.assertTrue('update_time' in account)
            self.assertTrue('create_time' in account)

            self.assertTrue('company_info' in staff)
            company = staff['company_info']
            self.assertTrue('id' in company)
            self.assertTrue('name' in company)
            self.assertTrue('license_number' in company)
            self.assertTrue('create_time' in company)

    def test_create_staff(self):
        api = 'staff.add'
        self.access_api(api=api, staff_info=json.dumps(self.staff_info))

    def test_search_staff(self):
        api = 'staff.search'
        current_page = 1
        result = self.access_api(
            api=api,
            current_page=current_page,
            search_info=json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)

        if result['total'] <= 0:
            self.test_create_staff()
            result = self.access_api(
                api=api,
                current_page=current_page,
                search_info=json.dumps({})
            )

        for staff in result['data_list']:
            self.assert_staff_fields(staff)
        return result['data_list']

    def test_get_staff(self):
        staff_list = self.test_search_staff()
        staff_id = staff_list[-1]['id']
        api = "staff.get"
        result = self.access_api(api=api, staff_id=staff_id)
        self.assertTrue('staff_info' in result)
        self.assert_staff_fields(result['staff_info'], False)

    def test_update_staff(self):
        staff_list = self.test_search_staff()
        staff_id = staff_list[-1]['id']
        api = "staff.update"
        self.access_api(
            api=api,
            staff_id=staff_id,
            staff_info=json.dumps(self.update_info)
        )
