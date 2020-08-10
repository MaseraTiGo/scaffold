# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase


class UniversityMajorTestCase(CrmAPITestCase):

    def setUp(self):
        self.major_info = {
            'name': '机械电子工程00222',
            'content': '机械电子工程是非常好的专业',
            'is_hot':0,
            'sort':0,
            'icons':''
        }
        self.update_info = {
            'name': '机械电子工程002',
            'content': '机械电子工程是非常好的专业2',
            'is_hot':0,
            'sort':1,
            'icons':''
        }

    def tearDown(self):
        pass

    def assert_major_fields(self, major, need_id = False):
        if need_id:
            self.assertTrue('id' in major)
        self.assertTrue('name' in major)
        self.assertTrue('content' in major)
        self.assertTrue('is_hot' in major)

    def test_create_major(self):
        api = 'university.major.add'
        self.access_api(
            api = api,
            major_info = json.dumps(self.major_info)
        )

    def test_search_major(self):
        api = 'university.major.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        if not len(result['data_list']):
            self.test_create_major()
            result = self.access_api(
                api = api,
                current_page = current_page,
                search_info = json.dumps({})
            )

        for major in result['data_list']:
            self.assert_major_fields(major, True)
        return result['data_list']

    def test_search_all_major(self):
        api = 'university.major.searchall'
        result = self.access_api(
            api = api,
        )
        self.assertTrue("data_list" in result)
        if not len(result['data_list']):
            self.test_create_major()
            result = self.access_api(
                api = api,
            )

        for major in result['data_list']:
            self.assert_major_fields(major, True)
        return result['data_list']

    def test_update_major(self):
        major_list = self.test_search_major()
        major_id = major_list[0]['id']
        api = "university.major.update"
        self.access_api(
            api = api,
            major_id = major_id,
            major_info = json.dumps(self.update_info)
        )

    def test_remove_major(self):
        major_list = self.test_search_major()
        major_id = major_list[0]['id']
        api = 'university.major.remove'
        result = self.access_api(
            api = api,
            major_id = major_id
        )

    def test_settop_major(self):
        major_list = self.test_search_major()
        major_id = major_list[0]['id']
        api = 'university.major.settop'
        result = self.access_api(
            api = api,
            major_id = major_id
        )