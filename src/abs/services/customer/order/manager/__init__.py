# coding=UTF-8
import json
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.order.manager import \
     OrderServer as mg_OrderServer
from abs.services.customer.order.store.order import Order
from abs.services.customer.order.store.orderitem import OrderItem
from abs.middleground.business.enterprise.manager import EnterpriseServer
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
        mg_search_info = {}
        if 'number' in search_info:
            number = search_info.pop('number')
            mg_search_info.update({"number":number})
        if 'status' in search_info:
            status = search_info.pop('status')
            mg_search_info.update({"status":status})
        if len(mg_search_info) > 0:
            order_id_list = mg_OrderServer.search_order_id_list(
                **mg_search_info
            )
            search_info.update({
                'mg_order_id__in': order_id_list
            })
        order_qs = Order.search(**search_info)
        return order_qs

    @classmethod
    def cancel(cls, order):
        if order.mg_order.status != OrderStatus.ORDER_LAUNCHED:
            raise BusinessError('待付款订单才能取消')
        mg_OrderServer.close(order.mg_order_id)


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

        order = Order.create(
            customer_id = customer.id,
            mg_order_id = mg_order.id,
            agent_id = agent.id,
            source = source
        )
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
        autograph_url, contract_url = image_middleware.get_contract(
            agent.name,
            agent.official_seal,
            base64_image,
            search_info['name']
        )
        search_info.update({
            'order_item_id': order_item.id,
            'agent_id': agent.id,
            'autograph': autograph_url,
            'url': json.dumps([contract_url])
        })
        contract = Contract.create(**search_info)
        mg_OrderServer.finish(order_item.order.mg_order_id)

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

