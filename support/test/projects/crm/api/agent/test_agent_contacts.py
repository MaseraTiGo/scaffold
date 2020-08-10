# coding=UTF-8

import json
import hashlib
from support.common.testcase.crm_api_test_case import CrmAPITestCase
from support.common.generator.field.model.entity import AgentEntity


class AgentContactsTestCase(CrmAPITestCase):

    def setUp(self):
        self.agent = AgentEntity().generate()
        self.contacts_info = {
            "contacts":"宁缺",
            "phone":"13300000001",
            "email":"2323333@qq.com",
            "gender":"man",
        }
        self.update_info = {
            "contacts":"宁缺001",
            "phone":"13300000001",
            "email":"2323333@qq.com",
            "gender":"man",
        }

    def tearDown(self):
        pass

    def assert_contacts_fields(self, contacts, need_id = False):
        if need_id:
            self.assertTrue('id' in contacts)
        self.assertTrue('contacts' in contacts)
        self.assertTrue('phone' in contacts)
        self.assertTrue('email' in contacts)
        self.assertTrue('gender' in contacts)
        self.assertTrue('account_status' in contacts)
        self.assertTrue('create_time' in contacts)

    def test_create_contacts(self):
        api = 'agent.contacts.add'
        self.access_api(
            api = api,
            agent_id = self.agent.id,
            contacts_info = json.dumps(self.contacts_info)
        )

    def test_search_contacts(self):
        api = 'agent.contacts.search'
        current_page = 1
        result = self.access_api(
            api = api,
            agent_id = self.agent.id,
            current_page = current_page,
            search_info = json.dumps({})
        )
        self.assertTrue("data_list" in result)
        self.assertTrue("total" in result)
        self.assertTrue("total_page" in result)
        if not len(result['data_list']):
            self.test_create_contacts()
            result = self.access_api(
                api = api,
                agent_id = self.agent.id,
                current_page = current_page,
                search_info = json.dumps({})
            )
        for contacts in result['data_list']:
            self.assert_contacts_fields(contacts, True)
        return result['data_list']

    def test_update_contacts(self):
        contacts_list = self.test_search_contacts()
        contacts_id = contacts_list[0]['id']
        api = "agent.contacts.update"
        self.access_api(
            api = api,
            contacts_id = contacts_id,
            contacts_info = json.dumps(self.update_info)
        )

    def test_createaccount_contacts(self):
        contacts_list = self.test_search_contacts()
        contacts_id = contacts_list[0]['id']
        contacts_info = {
            "account":contacts_list[0]["phone"],
            "password":hashlib.md5("123456".encode('utf8')).hexdigest(),
        }
        api = "agent.contacts.addaccount"
        self.access_api(
            api = api,
            contacts_id = contacts_id,
            contacts_info = json.dumps(contacts_info)
        )

