# coding=UTF-8
'''
Created on 2020年7月23日

@author: Roy
'''


from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.base.api import NoAuthorizedApi
from abs.middleground.business.transaction.utils.constant import \
        PayTypes, OwnTypes
from abs.middleground.business.merchandise.utils.constant import \
        DespatchService
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.middleground.business.order.manager import OrderServer


class Search(NoAuthorizedApi):
    """
    搜索订单
    """
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(
        IntField,
        desc="当前页码"
    )
    request.search_info = RequestField(
        DictField,
        desc="搜索订单条件",
        conf={
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")
    response.data_list = ResponseField(
        ListField,
        desc="订单列表",
        fmt=DictField(
            desc="订单详情",
            conf={
                'id': IntField(desc="订单id"),
                'number': CharField(desc="订单编号"),
                'description': CharField(desc="订单描述"),
                'remark': CharField(desc="订单备注"),
                'status': CharField(
                    desc="订单状态",
                    choices=OrderStatus.CHOICES
                ),
                'sale_price': IntField(desc="订单金额，单位：分"),
                'strike_price': IntField(desc="成交金额，单位：分"),
                'actual_amount': CharField(desc="实付金额,单位：分"),
                'create_time': DatetimeField(desc="订单创建时间"),
                'snapshoot_list': ListField(
                    desc='订单列表',
                    fmt=DictField(
                        desc="订单详情",
                        conf={
                            'id': CharField(desc="订单快照id"),
                            'title': CharField(desc="订单标题"),
                            'show_image': CharField(desc="订单图片"),
                            'sale_price': IntField(desc="订单单价"),
                            'count': IntField(desc="订单数量"),
                            'total_price': IntField(desc="总价"),
                        }
                    )
                ),
                'payment_list': ListField(
                    desc='支付列表',
                    fmt=DictField(
                        desc="支付详情",
                        conf={
                            'id': CharField(desc="支付id"),
                            'remark': CharField(desc="支付备注"),
                            'pay_type': CharField(
                                desc="支付类型",
                                choices=PayTypes.CHOICES
                            ),
                            'amount': IntField(desc="支付金额"),
                            'output_record_id': IntField(desc="账务出账单ID"),
                            'create_time': DatetimeField(desc="支付时间"),
                        }
                    )
                ),
                'delivery_list': ListField(
                    desc='发货列表',
                    fmt=DictField(
                        desc="发货详情",
                        conf={
                            'id': CharField(desc="发货id"),
                            'despatch_type': CharField(
                                desc="发货方式",
                                choices=DespatchService.CHOICES
                            ),
                            'remark': CharField(desc="发货备注"),
                            'despatch_id': IntField(desc="发货业务ID"),
                            'create_time': DatetimeField(desc="支付时间"),
                        }
                    )
                ),
            }
        )
    )
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "搜索订单"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        order_spliter = OrderServer.search(
            request.current_page,
            is_hung=True,
            **request.search_info
        )
        return order_spliter

    def fill(self, response, order_spliter):
        data_list = [{
            'id': order.id,
            'number': order.number,
            'description': order.description,
            'remark': order.remark,
            'status': order.status,
            'sale_price': order.requirement.sale_price,
            'strike_price': order.strike_price,
            'actual_amount': order.payment.actual_amount,
            'create_time': order.create_time,
            'snapshoot_list': [
                {
                    'id': snapshoot.id,
                    'title': snapshoot.title,
                    'show_image': snapshoot.show_image,
                    'sale_price': snapshoot.sale_price,
                    'count': snapshoot.count,
                    'total_price': snapshoot.total_price,
                }
                for snapshoot in order.requirement.snapshoot_list
            ],
            'payment_list': [
                {
                    'id': record.id,
                    'remark': record.remark,
                    'pay_type': record.pay_type,
                    'amount': record.amount,
                    'output_record_id': record.output_record_id,
                    'create_time': record.create_time,
                }
                for record in order.payment.payment_list
            ],
            'delivery_list': [
                {
                    'id': delivery.id,
                    'despatch_type': delivery.despatch_type,
                    'despatch_id': delivery.despatch_id,
                    'remark': delivery.remark,
                    'create_time': delivery.create_time,
                }
                for delivery in order.invoice.delivery_list
            ]
        } for order in order_spliter.data]
        response.data_list = data_list
        response.total = order_spliter.total
        response.total_page = order_spliter.total_page
        return response


class Get(NoAuthorizedApi):
    """
    获取订单详情
    """
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc="订单id")

    response = with_metaclass(ResponseFieldSet)
    response.order_info = ResponseField(
        DictField,
        desc="订单详情",
        conf={
            'id': IntField(desc="订单id"),
            'number': CharField(desc="订单编号"),
            'description': CharField(desc="订单描述"),
            'remark': CharField(desc="订单备注"),
            'status': CharField(
                desc="订单状态",
                choices=OrderStatus.CHOICES
            ),
            'sale_price': IntField(desc="订单金额，单位：分"),
            'strike_price': IntField(desc="成交金额，单位：分"),
            'actual_amount': CharField(desc="实付金额,单位：分"),
            'create_time': DatetimeField(desc="订单创建时间"),
            'snapshoot_list': ListField(
                desc='订单列表',
                fmt=DictField(
                    desc="订单详情",
                    conf={
                        'id': CharField(desc="订单快照id"),
                        'title': CharField(desc="订单标题"),
                        'show_image': CharField(desc="订单图片"),
                        'sale_price': IntField(desc="订单单价"),
                        'count': IntField(desc="订单数量"),
                        'total_price': IntField(desc="总价"),
                    }
                )
            ),
            'payment_list': ListField(
                desc='支付列表',
                fmt=DictField(
                    desc="支付详情",
                    conf={
                        'id': CharField(desc="支付id"),
                        'remark': CharField(desc="支付备注"),
                        'pay_type': CharField(
                            desc="支付类型",
                            choices=PayTypes.CHOICES
                        ),
                        'amount': IntField(desc="支付金额"),
                        'output_record_id': IntField(desc="账务出账单ID"),
                        'create_time': DatetimeField(desc="支付时间"),
                    }
                )
            ),
            'delivery_list': ListField(
                desc='发货列表',
                fmt=DictField(
                    desc="发货详情",
                    conf={
                        'id': CharField(desc="发货id"),
                        'despatch_type': CharField(
                            desc="发货方式",
                            choices=DespatchService.CHOICES
                        ),
                        'remark': CharField(desc="发货备注"),
                        'despatch_id': IntField(desc="发货业务ID"),
                        'create_time': DatetimeField(desc="支付时间"),
                    }
                )
            ),
        }
    )

    @classmethod
    def get_desc(cls):
        return "获取订单详情接口"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        return OrderServer.get(request.order_id, is_hung=True)

    def fill(self, response, order):
        response.order_info = {
            'id': order.id,
            'number': order.number,
            'description': order.description,
            'remark': order.remark,
            'status': order.status,
            'sale_price': order.requirement.sale_price,
            'strike_price': order.strike_price,
            'actual_amount': order.payment.actual_amount,
            'create_time': order.create_time,
            'snapshoot_list': [
                {
                    'id': snapshoot.id,
                    'title': snapshoot.title,
                    'show_image': snapshoot.show_image,
                    'sale_price': snapshoot.sale_price,
                    'count': snapshoot.count,
                    'total_price': snapshoot.total_price,
                }
                for snapshoot in order.requirement.snapshoot_list
            ],
            'payment_list': [
                {
                    'id': record.id,
                    'remark': record.remark,
                    'pay_type': record.pay_type,
                    'amount': record.amount,
                    'output_record_id': record.output_record_id,
                    'create_time': record.create_time,
                }
                for record in order.payment.payment_list
            ],
            'delivery_list': [
                {
                    'id': delivery.id,
                    'despatch_type': delivery.despatch_type,
                    'despatch_id': delivery.despatch_id,
                    'remark': delivery.remark,
                    'create_time': delivery.create_time,
                }
                for delivery in order.invoice.delivery_list
            ]
        }
        return response


class Place(NoAuthorizedApi):
    """
    下单
    """
    request = with_metaclass(RequestFieldSet)
    request.order_info = RequestField(
        DictField,
        desc="下单信息",
        conf={
            'remark': CharField(desc="备注"),
            'launch_type': CharField(
                desc="发起者类型",
                choices=OwnTypes.CHOICES
            ),
            'launch_id': CharField(desc="发起者id"),
            'server_type': CharField(
                desc="接收者类型",
                choices=OwnTypes.CHOICES
            ),
            'server_id': CharField(desc="接收者id"),
            'invoice_baseinfos': DictField(
                desc="收货基本信息",
                conf={
                    'name': CharField(desc="姓名", is_required=False),
                    'phone': CharField(desc="电话", is_required=False),
                    'address': CharField(desc="地址", is_required=False),
                    'identification': CharField(desc="身份证", is_required=False),
                }
            ),
            'specification_list': ListField(
                desc="购买列表",
                fmt=DictField(
                    desc="购买信息",
                    conf={
                        'id': IntField(desc="规格id"),
                        'count': IntField(desc="购买数量"),
                    }
                )
            ),
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.order_id = ResponseField(IntField, desc="订单Id")

    @classmethod
    def get_desc(cls):
        return "订单下单"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        specification_mapping = {
            specification.id: specification.count
            for specification in request.order_info.specification_list
        }
        specification_list = []
        order_total = 0
        for specification in MerchandiseServer.get_specification_list(
            specification_mapping.keys()
        ):
            count = specification_mapping[specification.id]
            specification.order_count = count
            specification.total_price = count * specification.sale_price
            order_total += specification.total_price
            specification_list.append(specification)

        order = OrderServer.place(
            specification_list,
            order_total,
            request.order_info.remark,
            request.order_info.launch_type,
            request.order_info.launch_id,
            request.order_info.server_type,
            request.order_info.server_id,
            **request.order_info.invoice_baseinfos,
        )
        return order

    def fill(self, response, order):
        response.order_id = order.id
        return response


class Pay(NoAuthorizedApi):
    """
    订单支付
    """
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc="订单ID")
    request.pay_info = RequestField(
        DictField,
        desc="支付信息",
        conf={
            'amount': IntField(desc="支付金额，单位：分"),
            'pay_type': CharField(desc="支付类型", choices=PayTypes.CHOICES),
            'remark': CharField(desc="支付备注"),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "订单支付"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        OrderServer.pay(
            request.order_id,
            amount=request.pay_info.amount,
            pay_type=request.pay_info.pay_type,
            remark=request.pay_info.remark,
        )

    def fill(self, response):
        return response


class Delivery(NoAuthorizedApi):
    """
    订单发货
    """
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc="订单id")
    request.delivery_info = RequestField(
        DictField,
        desc="发货详情",
        conf={
            "despatch_type": CharField(
                desc="发货方式",
                choices=DespatchService.CHOICES,
            ),
            "remark": CharField(desc="备注"),
            'invoice_baseinfos': DictField(
                desc="收货基本信息",
                conf={
                    'name': CharField(desc="姓名", is_required=False),
                    'phone': CharField(desc="电话", is_required=False),
                    'address': CharField(desc="地址", is_required=False),
                    'identification': CharField(desc="身份证", is_required=False),
                }
            ),
            "snapshoot_list": ListField(
                desc="发货订单列表",
                fmt=DictField(
                    desc="发货订单详情",
                    conf={
                        "id": IntField(desc="快照订单id"),
                        "count": IntField(desc="发货订单数量"),
                    }
                )
            ),
        }
    )

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "订单发货"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        despatch_id = 0
        snapshoot_mapping = {
            snapshoot.id: snapshoot.count
            for snapshoot in request.delivery_info.snapshoot_list
        }
        OrderServer.delivery(
            request.order_id,
            request.delivery_info.despatch_type,
            despatch_id,
            request.delivery_info.remark,
            snapshoot_mapping,
            **request.delivery_info.invoice_baseinfos
        )

    def fill(self, response):
        return response


class Finish(NoAuthorizedApi):
    """
    完成订单
    """
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc="订单id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "完成订单"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        OrderServer.finish(request.order_id)

    def fill(self, response):
        return response


class Close(NoAuthorizedApi):
    """
    关闭订单
    """
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc="订单id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "关闭订单"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        OrderServer.close(request.order_id)

    def fill(self, response):
        return response
