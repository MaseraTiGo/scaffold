# coding=UTF-8

import json
from random import choice
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerMessageTest(CustomerAPITestCase):

    def setUp(self):
        ...

    def tearDown(self):
        ...

    def get_random_data(self, data_list, only_id=True):
        if not data_list:
            return None
        return choice(data_list) if not only_id else choice(data_list)['id']

    def test_message_search(self):
        api = 'message.search'
        current_page = 1,
        result = self.access_api(api=api, current_page=current_page)
        for item in result.get('data_list', []):
            self.assertTrue('id' in item.keys())
            self.assertTrue('title' in item.keys())
            self.assertTrue('content' in item.keys())
            self.assertTrue('create_time' in item.keys())
        return result['data_list']

    def test_message_change_status(self):
        api = 'message.changestatus'
        data_list = self.test_message_search()
        message_id = self.get_random_data(data_list)
        if not message_id:
            print('no data 4 changing status')
            return
        print(f'current message id is===>{message_id}')
        result = self.access_api(api=api, message_id=message_id)

    def test_message_unread_count(self):
        api = 'message.unreadcount'
        result = self.access_api(api=api)
        print(f'unread message count: {result}')
        self.assertTrue(isinstance(result.get('unread_count'), int))
