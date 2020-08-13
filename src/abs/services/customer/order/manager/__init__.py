# coding=UTF-8
import json
import datetime
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.order.manager import \
     OrderServer as mg_OrderServer
from abs.services.customer.order.store.order import Order
from abs.services.customer.order.store.orderitem import OrderItem
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.middleware.pay import pay_middleware
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.middleware.image import image_middleware
from abs.services.customer.order.store.contract import Contract


class OrderServer(BaseManager):

    @classmethod
    def get(cls, order_id):
        order = Order.get_byid(order_id)
        if order is None:
            raise BusinessError("此订单不存在")
        order.mg_order = mg_OrderServer.get(
                            order.mg_order_id, is_hung = True
                         )
        return order

    @classmethod
    def search(cls, current_page, **search_info):
        order_qs = cls.search_all(**search_info).\
                    order_by("-create_time")
        splitor = Splitor(current_page, order_qs)
        splitor.data = mg_OrderServer.hung_order(splitor.get_list())
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        order_qs = Order.search(**search_info)
        return order_qs

    @classmethod
    def cancel(cls, order):
        mg_OrderServer.close(order.mg_order_id)
        snapshoot_list = mg_OrderServer.search_all_snapshoot(
            requirement = order.mg_order.requirement
        )
        for snapshoot in snapshoot_list:
            specification = MerchandiseServer.get_specification(
                snapshoot.specification_id
            )
            specification.update(stock = specification.stock + snapshoot.count)

    @classmethod
    def auto_cancel(cls):
        expire_time = datetime.datetime.now() - datetime.timedelta(minutes = 30)
        order_list = Order.search(
            status = OrderStatus.ORDER_LAUNCHED,
            create_time__lt = expire_time
        )
        mg_OrderServer.hung_order(order_list)
        for order in order_list:
            order.update(status = OrderStatus.ORDER_CLOSED)
            cls.cancel(order)

    @classmethod
    def add(
        cls,
        agent,
        customer,
        address,
        source,
        strike_price,
        specification_list
    ):
        invoice_baseinfos = {}
        if address:
            invoice_baseinfos = {
                'name': address.contacts,
                'phone': address.phone,
                'address': '-'.join([address.city, address.address])
            }
        mg_order = mg_OrderServer.place(
            specification_list,
            strike_price,
            '',
            'person',
            customer.person_id,
            'company',
            agent.company_id,
            **invoice_baseinfos
        )

        create_info = {
            'customer_id': customer.id,
            'mg_order_id': mg_order.id,
            'agent_id': agent.id,
            'source': source,
            'number': mg_order.number,
            'status': mg_order.status
        }
        if address:
            create_info.update({
                'name': address.contacts,
                'phone': address.phone
            })
        order = Order.create(**create_info)
        mapping = {}
        for specification in specification_list:
            mapping.update({
                specification.id: specification
            })
        snapshoot_list = mg_OrderServer.search_all_snapshoot(
            requirement = mg_order.requirement
        )
        for snapshoot in snapshoot_list:
            specification = mapping.get(snapshoot.specification_id)
            OrderItem.create(
                order = order,
                goods_id = specification.merchandise.goods.id,
                merchandise_snapshoot_id = snapshoot.id,
                school_name = specification.merchandise.goods.school.name,
                school_city = specification.merchandise.goods.school.city,
                major_name = specification.merchandise.goods.major.name,
                duration = specification.merchandise.goods.duration
            )
            specification.update(
                stock = specification.stock - specification.order_count
            )
        return order

    @classmethod
    def pay(cls, order, pay_type):
        number = mg_OrderServer.pay(
            order.mg_order.id,
            order.mg_order.strike_price,
            pay_type,
            ''
        )
        prepay_id = pay_middleware.pay_order(
            pay_type,
            number,
            order.mg_order.strike_price
        )
        return prepay_id

    @classmethod
    def pay_success_callback(cls, output_record_number):
        mg_order = mg_OrderServer.pay_success_callback(
            output_record_number
        )
        order = cls.search_all(mg_order_id = mg_order.id).first()
        order.update(
            status = mg_order.status,
            last_payment_time = mg_order.payment.last_payment_time
        )


class OrderItemServer(BaseManager):

    @classmethod
    def search_all(cls, **search_info):
        orderitem_qs = OrderItem.search(**search_info)
        return orderitem_qs

    @classmethod
    def hung_order_item(cls, order_list):
        order_mapping = {}
        for order in order_list:
            order.orderitem_list = []
            order_mapping[order.id] = order
        orderitem_list = list(cls.search_all(
                                 order_id__in = order_mapping.keys())
                              )
        mg_OrderServer.hung_snapshoot(orderitem_list)
        for orderitem in orderitem_list:
            if orderitem.order_id in order_mapping:
                order_mapping[orderitem.order_id].orderitem_list.\
                append(orderitem)
        return order_list

    @classmethod
    def get(cls, order_item_id):
        order_item = OrderItem.get_byid(order_item_id)
        if order_item:
            return order_item
        raise BusinessError('订单详情不存在')


class ContractServer(BaseManager):

    @classmethod
    def create(cls, order_item, agent, **search_info):
        base64_image = search_info.pop('autograph')
        autograph_url, contract_url, contract_img_url = image_middleware.get_contract(
            agent.name,
            agent.official_seal,
            base64_image,
            search_info['name']
        )
        search_info.update({
            'order_item_id': order_item.id,
            'agent_id': agent.id,
            'autograph': autograph_url,
            'url': json.dumps([contract_url]),
            'img_url': json.dumps([contract_img_url])
        })
        contract = Contract.create(**search_info)
        mg_OrderServer.finish(order_item.order.mg_order_id)
        order_item.order.update(status = OrderStatus.ORDER_FINISHED)
        return contract

    @classmethod
    def search_all(cls, **search_info):
        return Contract.search(**search_info)

    @classmethod
    def search(cls, current_page, **search_info):
        contract_qs = cls.search_all(**search_info).\
                      order_by("-create_time")
        splitor = Splitor(current_page, contract_qs)
        return splitor

