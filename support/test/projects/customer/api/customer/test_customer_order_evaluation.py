# coding=UTF-8
import json
from support.common.testcase.customer_api_test_case import CustomerAPITestCase


class CustomerOrderTest(CustomerAPITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_evaluation_add(self):
        api = 'customer.order.addevaluation'
        evaluation_info = json.dumps({
            'tags': '["good", "nice"]',
            'content': 'such a damn goods',
            'server_attitude': 2,
            'course_quality': 3,
            'major': 4,
        })
        order_item_id = 1
        self.access_api(api=api, order_item_id=order_item_id, evaluation_info=evaluation_info)

    def test_evaluation_all_search(self):
        api = 'customer.order.allevaluations'
        goods_id = 3
        result = self.access_api(api=api, current_page=1, goods_id=goods_id)
        # print('all evaluations==========>', result)
        self.assertTrue('data_list' in result)
        if result.get('data_list'):
            self.assertTrue('content' in result.get('data_list')[0])

    def test_get_evaluation_search(self):
        api = 'customer.order.getevaluation'
        order_item_id = 1
        result = self.access_api(api=api, order_item_id=order_item_id)
        self.assertTrue('content' in result.get('data'))

    def test_my_evaluation_search(self):
        api = 'customer.order.myevaluations'
        result = self.access_api(api=api, current_page=1)
        self.assertTrue('data_list' in result)
        if result.get('data_list'):
            self.assertTrue('content' in result.get('data_list')[0])

    def test_search_evaluations(self):
        api = 'customer.order.searchevaluations'
        goods_id = 3
        search_info = {
            'has_videos': True,
        }
        result = self.access_api(api=api, current_page=1, goods_id=goods_id, search_info=json.dumps(search_info))
        print('all evaluations==========>', result)
        self.assertTrue('data_list' in result)
        if result.get('data_list'):
            self.assertTrue('content' in result.get('data_list')[0])
