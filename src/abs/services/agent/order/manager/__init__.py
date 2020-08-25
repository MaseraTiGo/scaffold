# coding=UTF-8
import json
import datetime
import time
import random
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.order.manager import \
     OrderServer as mg_OrderServer
from abs.services.agent.order.store.order import Order
from abs.services.agent.order.store.orderitem import OrderItem
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.middleware.pay import pay_middleware
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.middleware.image import image_middleware
from abs.services.agent.order.store.contract import Contract


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
        agent_customer,
        invoice_info,
        source,
        strike_price,
        specification_list
    ):
        # invoice_baseinfos = {}
        # if address:
        #     invoice_baseinfos = {
        #         'name': address.contacts,
        #         'phone': address.phone,
        #         'address': '-'.join([address.city, address.address])
        #     }
        mg_order = mg_OrderServer.place(
            specification_list,
            strike_price,
            '',
            'person',
            agent_customer.person_id,
            'company',
            agent_customer.agent.company_id,
            **invoice_info
        )

        create_info = {
            'agent_customer_id': agent_customer.id,
            'mg_order_id': mg_order.id,
            'agent_id': agent_customer.agent_id,
            'person_id': agent_customer.person_id,
            'company_id': agent_customer.agent.company_id,
            'source': source,
            'number': mg_order.number,
            'status': mg_order.status,
            'name': invoice_info.get('name'),
            'phone': invoice_info.get('phone')
        }
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
                duration = specification.merchandise.goods.years.duration,
                category = specification.merchandise.goods.years.category
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

    @classmethod
    def pay_fail_callback(cls, output_record_number):
        mg_OrderServer.pay_fail_callback(output_record_number)


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
    def create(cls, order_item, agent, contacts):
        number = 'Sn_200' + str(int(time.time())) + str(random.randint(10000, 99999))
        mg_order = mg_OrderServer.get(order_item.order.mg_order_id)
        mg_OrderServer.hung_snapshoot([order_item])
        contract_img_url = image_middleware.get_contract(
            number,
            agent.name,
            contacts.contacts,
            contacts.phone,
            agent.official_seal,
            mg_order.invoice.name,
            mg_order.invoice.identification,
            order_item.snapshoot.brand_name,
            order_item.snapshoot.production_name,
            order_item.school_name,
            order_item.major_name,
            str(mg_order.strike_price/100)
        )
        create_info = {
            'name': mg_order.invoice.name,
            'phone': mg_order.invoice.phone,
            'identification': mg_order.invoice.identification,
            'email': '',
            'number': number,
            'agent_customer_id': order_item.order.agent_customer_id,
            'person_id': order_item.order.person_id,
            'company_id': order_item.order.company_id,
            'order_item_id': order_item.id,
            'agent_id': agent.id,
            'img_url': json.dumps(contract_img_url)
        }
        contract = Contract.create(**create_info)

        return contract

    @classmethod
    def autograph(cls, contract, autograph_img, email):
        autograph_url, contract_url, contract_img_url = image_middleware.autograph(
            contract.name,
            contract.phone,
            autograph_img,
            json.loads(contract.img_url)
        )
        contract.update(**{
            'email': email,
            'autograph': autograph_url,
            'url': json.dumps([contract_url]),
            'img_url': json.dumps(contract_img_url)
        })
        mg_OrderServer.finish(
            contract.order_item.order.mg_order_id
        )
        contract.order_item.order.update(
            status=OrderStatus.ORDER_FINISHED
        )

    @classmethod
    def search_all(cls, **search_info):
        return Contract.search(**search_info)

    @classmethod
    def search(cls, current_page, **search_info):
        contract_qs = cls.search_all(**search_info).\
                      order_by("-create_time")
        splitor = Splitor(current_page, contract_qs)
        return splitor

    @classmethod
    def get(cls, contract_id):
        contract = Contract.get_byid(contract_id)
        if contract:
            return contract
        raise BusinessError('合同不存在')

