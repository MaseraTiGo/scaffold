# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class UniversitySchoolTestCase(CrmAPITestCase):

    def setUp(self):
        self.school_info = {
            'name': '武汉科技大学001',
            'logo_url': 'logo',
            'content': '武汉科技大学是一所非常好的学校',
            'province':"湖北省",
            'city':"武汉市",
            'is_hot':0
        }
        self.school_info = {
            'name': '武汉科技大学002',
            'logo_url': 'logo2',
            'content': '武汉科技大学是一所非常好的学校',
            'province':"湖北省",
            'city':"武汉市",
            'is_hot':0
        }

    def tearDown(self):
        pass

    def assert_school_fields(self, school, need_id=False):
        if need_id:
            self.assertTrue('id' in school)
        self.assertTrue('name' in school)
        self.assertTrue('logo_url' in school)
        self.assertTrue('content' in school)
        self.assertTrue('province' in school)
        self.assertTrue('city' in school)
        self.assertTrue('is_hot' in school)

    def test_create_school(self):
        api = 'university.school.add'
        self.access_api(
            api=api,
            school_info=json.dumps(self.school_info)
        )

    def test_search_school(self):
        api = 'university.school.search'
        current_page = 1
        result = self.access_api(
            api=api,
            current_page=current_page,
            search_info=json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        if not len(result['data_list']):
            self.test_create_school()
            result = self.access_api(
                api=api,
                current_page=current_page,
                search_info=json.dumps({})
            )

        for school in result['data_list']:
            self.assert_school_fields(school, True)
        return result['data_list']

    def test_search_all_school(self):
        api = 'university.school.searchall'
        result = self.access_api(
            api=api,
        )
        self.assertTrue("data_list" in result)
        if not len(result['data_list']):
            self.test_create_school()
            result = self.access_api(
                api=api,
            )

        for school in result['data_list']:
            self.assert_school_fields(school, True)
        return result['data_list']

    def test_update_school(self):
        school_list = self.test_search_school()
        school_id = school_list[0]['id']
        api = "university.school.update"
        self.access_api(
            api=api,
            school_id=school_id,
            school_info=json.dumps(self.school_info)
        )

    def test_remove_school(self):
        school_list = self.test_search_school()
        school_id = school_list[0]['id']
        api = 'university.school.remove'
        result = self.access_api(
            api=api,
            school_id=school_id
        )

    def test_settop_school(self):
        school_list = self.test_search_school()
        school_id = school_list[0]['id']
        api = 'university.school.settop'
        result = self.access_api(
            api=api,
            school_id=school_id
        )