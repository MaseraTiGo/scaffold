# coding=UTF-8


from infrastructure.core.field.base import CharField, DictField, ListField, \
    IntField, DatetimeField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.customer.manager.api import CustomerAuthorizedApi
from abs.middleground.business.person.manager import PersonServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from infrastructure.core.exception.business_error import BusinessError
from abs.services.crm.production.manager import GoodsServer
from abs.services.crm.order.manager import OrderServer, OrderItemServer
from abs.middleground.business.order.manager import OrderServer as mg_OrderServer
from abs.services.crm.university.manager import UniversityServer
from abs.middleground.business.production.manager import ProductionServer


class Add(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_info = RequestField(DictField, desc="订单详情", conf={
        'strike_price': IntField(desc="金额"),
        'address_id': IntField(desc="收货地址id"),
        'goods_list': ListField(
            desc='商品列表',
            fmt=DictField(
                desc='商品信息',
                conf={
                    'quantity': IntField(desc="购买数量"),
                    'specification_id': IntField(desc="规格id")
                }
            )
        )
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户下单接口"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        order_info = request.order_info
        customer = self.auth_user
        address = PersonServer.get_address(order_info.pop('address_id'))
        specification_list = []
        for goods_info in order_info['goods_list']:
            specification = MerchandiseServer.get_specification(goods_info['specification_id'])
            if specification.stock < goods_info['quantity']:
                raise BusinessError('库存不足')
            if specification.merchandise.use_status != 'enable':
                raise BusinessError('商品已下架')
            specification.order_count = goods_info['quantity']
            specification.total_price = goods_info['quantity'] * specification.sale_price
            specification_list.append(specification)
        GoodsServer.hung_goods([
            specification.merchandise
            for specification in specification_list]
        )
        UniversityServer.hung_school([
            specification.merchandise.goods
            for specification in specification_list]
        )
        UniversityServer.hung_major([
            specification.merchandise.goods
            for specification in specification_list]
        )
        OrderServer.add(customer, address, 'app', order_info['strike_price'], specification_list)

    def fill(self, response):
        return response


class Get(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc="订单id")

    response = with_metaclass(ResponseFieldSet)
    response.order_info = ResponseField(DictField, desc="订单信息", conf={
        'id': IntField(desc="订单id"),
        'number': IntField(desc="订单编号"),
        'status': CharField(desc="订单状态"),
        'strike_price': IntField(desc="价格"),
        'create_time': DatetimeField(desc="下单时间"),
        'last_payment_type': CharField(desc='付款方式'),
        'last_payment_time': CharField(desc="付款时间"),
        'last_payment_number': CharField(desc="最后付款单号"),
        'order_item_list': ListField(
            desc="商品列表",
            fmt=DictField(
                desc="商品",
                conf={
                    'sale_price': IntField(desc="单价"),
                    'total_price': IntField(desc="总价"),
                    'quantity': IntField(desc="数量"),
                    'show_image': CharField(desc="展示图片"),
                    'title': CharField(desc="标题"),
                    'school_name': CharField(desc="学校名称"),
                    'major_name': CharField(desc="专业名称"),
                    'duration': CharField(desc="学年"),
                    'school_city': CharField(desc="学校城市"),
                    'brand_name': CharField(desc="品牌"),
                    'production_name': CharField(desc="产品名"),
                    'specification_value_list': ListField(
                        desc="商品规格值",
                        fmt=DictField(
                            desc='规格值',
                            conf={
                                'category': CharField(desc="属性分类"),
                                'attribute': CharField(desc="属性值")
                            }
                        )
                    )
                }
            )
        )
    })

    @classmethod
    def get_desc(cls):
        return "订单详情"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        order = OrderServer.get(request.goods_id)
        if order.customer_id != self.auth_user.id:
            raise BusinessError('订单异常')
        order.order_item_list = OrderItemServer.search_all(order=order)
        mg_OrderServer.hung_snapshoot(order.order_item_list)
        MerchandiseServer.hung_specification([
            order_item.snapshoot
            for order_item in order.order_item_list
        ])
        ProductionServer.hung_production([
            order_item.snapshoot
            for order_item in order.order_item_list
        ])
        return order

    def fill(self, response, order):
        response.order_info = {
            'id': order.id,
            'number': order.mg_order.number,
            'status': order.mg_order.status,
            'strike_price': order.mg_order.strike_price,
            'create_time': order.mg_order.create_time,
            'last_payment_type': order.mg_order.last_payment_type,
            'last_payment_time': order.mg_order.last_payment_time,
            'last_payment_number': '',
            'order_item_list': [{
                'sale_price': order_item.snapshoot.sale_price,
                'total_price': order_item.snapshoot.total_price,
                'quantity': order_item.snapshoot.count,
                'show_image': order_item.snapshoot.show_image,
                'title': order_item.snapshoot.title,
                'school_name': order_item.school_name,
                'major_name': order_item.major_name,
                'duration': order_item.get_duration_display(),
                'school_city': order_item.school_city,
                'brand_name': order_item.snapshoot.production.brand.name,
                'production_name': order_item.snapshoot.production.name,
                'specification_value_list': [{
                    'category': specification_value.category,
                    'attribute': specification_value.attribute
                } for specification_value
                    in order_item.specification.specification_value_list]
            } for order_item in order.order_item_list]
        }
        return response


class Search(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前页码")
    request.search_info = RequestField(
        DictField,
        desc="搜索订单",
        conf={
            'status': CharField(desc="订单状态", is_required=False)
        }
    )

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(
        ListField,
        desc="订单列表",
        fmt=DictField(
            desc="订单信息",
            conf={
                'id': IntField(desc="订单id"),
                'number': IntField(desc="订单编号"),
                'status': CharField(desc="订单状态"),
                'strike_price': IntField(desc="价格"),
                'create_time': DatetimeField(desc="下单时间"),
                'last_payment_type': CharField(desc='付款方式'),
                'last_payment_time': CharField(desc="付款时间"),
                'last_payment_number': CharField(desc="最后付款单号"),
                'order_item_list': ListField(
                    desc="商品列表",
                    fmt=DictField(
                        desc="商品",
                        conf={
                            'sale_price': IntField(desc="单价"),
                            'total_price': IntField(desc="总价"),
                            'quantity': IntField(desc="数量"),
                            'show_image': CharField(desc="展示图片"),
                            'title': CharField(desc="标题"),
                            'school_name': CharField(desc="学校名称"),
                            'major_name': CharField(desc="专业名称"),
                            'duration': CharField(desc="学年"),
                            'school_city': CharField(desc="学校城市"),
                            'brand_name': CharField(desc="品牌"),
                            'production_name': CharField(desc="产品名"),
                            'specification_value_list': ListField(
                                desc="商品规格值",
                                fmt=DictField(
                                    desc='规格值',
                                    conf={
                                        'category': CharField(desc="属性分类"),
                                        'attribute': CharField(desc="属性值")
                                    }
                                )
                            )
                        }
                    )
                )
            }
        )
    )
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "订单列表"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        page_list = OrderServer.search(request.current_page, **request.search_info)
        OrderItemServer.hung_order_item(page_list.data)
        all_order_item_list = []
        for order in page_list.data:
            all_order_item_list.extend(order.orderitem_list)
        mg_OrderServer.hung_snapshoot(all_order_item_list)
        MerchandiseServer.hung_specification([
            order_item.snapshoot
            for order_item in all_order_item_list
        ])
        ProductionServer.hung_production([
            order_item.snapshoot
            for order_item in all_order_item_list
        ])
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': order.id,
            'number': order.mg_order.number,
            'status': order.mg_order.status,
            'strike_price': order.mg_order.strike_price,
            'create_time': order.mg_order.create_time,
            'last_payment_type': order.mg_order.last_payment_type,
            'last_payment_time': order.mg_order.last_payment_time,
            'last_payment_number': '',
            'order_item_list': [{
                'sale_price': order_item.snapshoot.sale_price,
                'total_price': order_item.snapshoot.total_price,
                'quantity': order_item.snapshoot.count,
                'show_image': order_item.snapshoot.show_image,
                'title': order_item.snapshoot.title,
                'school_name': order_item.school_name,
                'major_name': order_item.major_name,
                'duration': order_item.get_duration_display(),
                'school_city': order_item.school_city,
                'brand_name': order_item.snapshoot.production.brand.name,
                'production_name': order_item.snapshoot.production.name,
                'specification_value_list': [{
                    'category': specification_value.category,
                    'attribute': specification_value.attribute
                } for specification_value
                    in order_item.specification.specification_value_list]
            } for order_item in order.orderitem_list]
        } for order in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response