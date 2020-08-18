# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase
from support.common.generator.field.model.entity import RelationsEntity


class UniversitySchoolYearsTestCase(CrmAPITestCase):

    def setUp(self):
        self.relations = RelationsEntity().generate()
        self.years_info = {
            'category': 'graduate',
            'duration': 'two_half_year',
        }
        self.update_info = {
            'category': 'specialty',
            'duration': 'two_year',
        }


    def tearDown(self):
        pass

    def assert_school_years_fields(self, years, need_id = False):
        if need_id:
            self.assertTrue('id' in years)
        self.assertTrue('category' in years)
        self.assertTrue('duration' in years)
        self.assertTrue('create_time' in years)


    def test_create_years(self):
        api = 'university.school.relations.years.add'
        self.access_api(
            api = api,
            relations_id = self.relations.id,
            years_info = json.dumps(self.years_info)
        )

    def test_search_years(self):
        api = 'university.school.relations.years.search'
        current_page = 1
        result = self.access_api(
            api = api,
            relations_id = self.relations.id,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        if not len(result['data_list']):
            self.test_create_years()
            result = self.access_api(
                api = api,
                relations_id = self.relations.id,
                years_info = json.dumps(self.years_info)
            )

        for years in result['data_list']:
            self.assert_school_years_fields(years, True)
        return result['data_list']

    def test_update_years(self):
        years_list = self.test_search_years()
        years_id = years_list[0]['id']
        api = "university.school.relations.years.update"
        self.access_api(
            api = api,
            years_id = years_id,
            years_info = json.dumps(self.update_info)
        )

    def test_remove_years(self):
        years_list = self.test_search_years()
        years_id = years_list[0]['id']
        api = 'university.school.relations.years.remove'
        result = self.access_api(
            api = api,
            years_id = years_id
        )
