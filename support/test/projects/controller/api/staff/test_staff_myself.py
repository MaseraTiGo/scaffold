# coding=UTF-8

import json

from support.common.testcase.controller_api_test_case import \
        ControllerAPITestCase


class StaffMyselfTestCase(ControllerAPITestCase):

    def setUp(self):
        self.update_info = {
            'name': '马冬梅',
            'work_number': 'Bq0003',
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

    def test_staff_myself(self):
        api = 'staff.myself.get'
        result = self.access_api(api)
        self.assertTrue('staff_info' in result)
        self.assert_staff_fields(result['staff_info'], False)

    def test_update_staff(self):
        api = "staff.myself.update"
        self.access_api(api=api, myself_info=json.dumps(self.update_info))
