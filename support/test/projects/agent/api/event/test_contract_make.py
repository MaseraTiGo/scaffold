# coding=UTF-8

import json
import random
from support.common.testcase.agent_api_test_case import AgentAPITestCase
from support.common.generator.field.model.entity import AgentCustomerEntity, \
     AgentCustomerChanceEntity
from abs.middleware.contract import contract_middleware
from abs.middleware.image import image_middleware
from abs.services.agent.contract.models import Template
from abs.services.crm.agent.models import Agent

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


    def test_create_track(self):
        agent = Agent.search(id = 1)[0]
        image_middleware.get_image(agent.official_seal)

