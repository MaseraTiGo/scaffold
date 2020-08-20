# coding=UTF-8

import json
import random
from support.common.testcase.agent_api_test_case import AgentAPITestCase
from support.common.generator.field.model.entity import AgentCustomerEntity, \
     AgentCustomerChanceEntity


class TrackEventTestCase(AgentAPITestCase):

    def setUp(self):
        self.sale_chance = AgentCustomerChanceEntity().generate()
        self.agent_customer = AgentCustomerEntity().generate()
        self.track_info = {
            'track_type': 'phone',
            'describe': '毫无兴趣',
            'remark':'',
        }


    def tearDown(self):
        pass

    def assert_track_fields(self, track, need_id = False):
        if need_id:
            self.assertTrue('id' in track)
        self.assertTrue('staff_name' in track)
        self.assertTrue('organization_name' in track)
        self.assertTrue('track_type' in track)
        self.assertTrue('describe' in track)
        self.assertTrue('remark' in track)
        self.assertTrue('create_time' in track)


    def test_create_track(self):
        api = 'event.track.add'
        agent_customer_id = self.agent_customer.id
        self.access_api(
            api = api,
            agent_customer_id = agent_customer_id,
            track_info = json.dumps(self.track_info)
        )


    def test_search_track(self):
        api = 'event.track.search'
        result = self.access_api(
            api = api,
            current_page = 1,
            sale_chance_id = self.sale_chance.id
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        for track in result['data_list']:
            self.assert_track_fields(track, True)
        return result['data_list']
