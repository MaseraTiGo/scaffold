# coding=UTF-8

import json
import random

from support.common.testcase.middleground_api_test_case import \
        MiddlegroundAPITestCase
from support.common.generator.field.model.entity import CrnCompanyEntitry,\
        CustomerEntity, SpecificationEntity


class MerchandiseTestCase(MiddlegroundAPITestCase):

    def setUp(self):
        crm = CrnCompanyEntitry().generate()
        customer = CustomerEntity().generate()
        specification_list = [
            SpecificationEntity().generate(),
        ]
        self.order_info = {
            'remark': "这是一个测试订单",
            'launch_type': 'person',
            'launch_id': customer.person_id,
            'server_type': 'company',
            'server_id': crm.id,
            'invoice_baseinfos': {
                'name': '杨荣凯',
                'phone': '155277031115',
                'address': '高新四路谷尚居',
            },
            'specification_list': [
                {
                    'id': specification.id,
                    'count': random.randint(2, 5)
                }
                for specification in specification_list
            ]
        }

    def tearDown(self):
        pass

    def assert_order_snapshoot_fields(self, snapshoot):
        self.assertTrue('id' in snapshoot)
        self.assertTrue('title' in snapshoot)
        self.assertTrue('show_image' in snapshoot)
        self.assertTrue('sale_price' in snapshoot)
        self.assertTrue('count' in snapshoot)
        self.assertTrue('total_price' in snapshoot)

    def assert_order_payment_fields(self, payment):
        self.assertTrue('id' in payment)
        self.assertTrue('remark' in payment)
        self.assertTrue('pay_type' in payment)
        self.assertTrue('amount' in payment)
        self.assertTrue('output_record_id' in payment)
        self.assertTrue('create_time' in payment)

    def assert_order_delivery_fields(self, delivery):
        self.assertTrue('id' in delivery)
        self.assertTrue('despatch_type' in delivery)
        self.assertTrue('despatch_id' in delivery)
        self.assertTrue('remark' in delivery)
        self.assertTrue('create_time' in delivery)

    def assert_order_fields(self, order, need_id=False):
        if need_id:
            self.assertTrue('id' in order)
        self.assertTrue('number' in order)
        self.assertTrue('description' in order)
        self.assertTrue('remark' in order)
        self.assertTrue('status' in order)
        self.assertTrue('sale_price' in order)
        self.assertTrue('strike_price' in order)
        self.assertTrue('actual_amount' in order)
        self.assertTrue('create_time' in order)
        self.assertTrue('snapshoot_list' in order)
        for snapshoot in order['snapshoot_list']:
            self.assert_order_snapshoot_fields(snapshoot)
        self.assertTrue('payment_list' in order)
        for payment in order['payment_list']:
            self.assert_order_payment_fields(payment)
        self.assertTrue('delivery_list' in order)
        for delivery in order['delivery_list']:
            self.assert_order_delivery_fields(delivery)

    def test_order_finished_workflow(self):
        # 1. 下单测试
        api = 'order.place'
        result = self.access_api(
            api=api,
            order_info=json.dumps(self.order_info)
        )
        self.assertTrue('order_id' in result)
        order_id = result['order_id']

        # 2. 支付测试
        api = 'order.pay'
        result = self.access_api(
            api=api,
            order_id=order_id,
            pay_info=json.dumps({
                'amount': 1300,
                'pay_type': 'bank',
                'remark': '测试支付',
            })
        )

        # 3. 获取订单测试
        api = 'order.get'
        result = self.access_api(
            api=api,
            order_id=order_id,
        )
        self.assertTrue('order_info' in result)
        order_info = result['order_info']
        self.assert_order_fields(order_info)

        # 4. 发货测试
        api = 'order.delivery'
        snapshoot_list = [
            {
                'id': snapshoot['id'],
                'count': random.randint(1, snapshoot['count']),
            }
            for snapshoot in order_info['snapshoot_list']
        ]
        result = self.access_api(
            api=api,
            order_id=order_id,
            delivery_info=json.dumps({
                'despatch_type': 'logistics',
                'remark': '货物已发送',
                'invoice_baseinfos': {
                    'name': '冯时宇',
                    'phone': '15527700001',
                    'identification': '152127199007020021',
                },
                'snapshoot_list': snapshoot_list
            })
        )

        # 5、 完成测试
        api = 'order.finish'
        result = self.access_api(
            api=api,
            order_id=order_id,
        )

        # 6、 搜索测试
        api = 'order.search'
        result = self.access_api(
            api=api,
            current_page=1,
            search_info=json.dumps({}),
        )
        self.assertTrue('total' in result)
        self.assertTrue('total_page' in result)
        self.assertTrue('data_list' in result)
        for data in result['data_list']:
            self.assert_order_fields(data)

    def test_order_closed_workflow(self):
        # 1. 下单测试
        api = 'order.place'
        result = self.access_api(
            api=api,
            order_info=json.dumps(self.order_info)
        )
        self.assertTrue('order_id' in result)
        order_id = result['order_id']

        # 2、 完成测试
        api = 'order.close'
        result = self.access_api(
            api=api,
            order_id=order_id,
        )

        # 3、 搜索测试
        api = 'order.search'
        result = self.access_api(
            api=api,
            current_page=1,
            search_info=json.dumps({}),
        )
        self.assertTrue('total' in result)
        self.assertTrue('total_page' in result)
        self.assertTrue('data_list' in result)
        for data in result['data_list']:
            self.assert_order_fields(data)
