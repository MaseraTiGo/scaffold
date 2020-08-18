# coding=UTF-8

import json

from support.common.testcase.crm_api_test_case import CrmAPITestCase
from support.common.generator.field.model.entity import SchoolEntity, \
     MajorEntity


class UniversitySchoolRelationsTestCase(CrmAPITestCase):

    def setUp(self):
        self.school = SchoolEntity().generate()
        self.major = MajorEntity().generate()
        self.years_list = [{
            'category': 'undergraduate',
            'duration': 'one_year',
        }]

    def tearDown(self):
        pass

    def assert_school_relations_fields(self, relations, need_id = False):
        if need_id:
            self.assertTrue('id' in relations)
        self.assertTrue('major_id' in relations)
        self.assertTrue('major_name' in relations)
        self.assertTrue('create_time' in relations)
        self.assertTrue('years_list' in relations)

    def test_create_relations(self):
        api = 'university.school.relations.add'
        self.access_api(
            api = api,
            shcool_id = self.school.id,
            relations_info = json.dumps({
                "major_id":self.major.id,
                "years_list":self.years_list
            })
        )

    def test_search_relations(self):
        api = 'university.school.relations.search'
        current_page = 1
        result = self.access_api(
            api = api,
            current_page = current_page,
            shcool_id = self.school.id,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        if not len(result['data_list']):
            self.test_create_relations()
            result = self.access_api(
                api = api,
                shcool_id = self.school.id,
                relations_info = json.dumps({
                    "major_id":self.major.id,
                    "years_list":self.years_list
                })
            )

        for relations in result['data_list']:
            self.assert_school_relations_fields(relations, True)
        return result['data_list']

    def test_update_relations(self):
        relations_list = self.test_search_relations()
        relations_id = relations_list[0]['id']
        api = "university.school.relations.update"
        self.access_api(
            api = api,
            relations_id = relations_id,
            relations_info = json.dumps({
                "major_id":self.major.id,
            })
        )

    def test_remove_relations(self):
        relations_list = self.test_search_relations()
        relations_id = relations_list[0]['id']
        api = 'university.school.relations.remove'
        result = self.access_api(
            api = api,
            relations_id = relations_id
        )

