# coding=UTF-8
import json
import datetime
import time
import random
from django.db.models import *
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.order.manager import \
     OrderServer as mg_OrderServer
from abs.services.agent.order.store import Order, OrderItem, Contract, Plan
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.middleware.pay import pay_middleware
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.middleware.contract import contract_middleware
from abs.middleware.image import image_middleware
from abs.middleware.email import email_middleware
from abs.middleware.config import config_middleware
from abs.middleground.business.merchandise.utils.constant import \
     DespatchService
from abs.services.agent.order.utils.constant import ContractStatus, PlanStatus
from abs.services.crm.contract.utils.constant import ValueSource


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
        order.update(status = OrderStatus.ORDER_CLOSED)

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
        deposit,
        strike_price,
        pay_services,
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
            'deposit':deposit,
            'agent_customer_id': agent_customer.id,
            'mg_order_id': mg_order.id,
            'agent_id': agent_customer.agent_id,
            'person_id': agent_customer.person_id,
            'company_id': agent_customer.agent.company_id,
            'source': source,
            'number': mg_order.number,
            'status': mg_order.status,
            'name': invoice_info.get('name'),
            'phone': invoice_info.get('phone'),
            'pay_services':pay_services
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
                category = specification.merchandise.goods.years.category,
                template_id = specification.merchandise.goods.template_id,
            )
            specification.update(
                stock = specification.stock - specification.order_count
            )
        return order

    @classmethod
    def paycode(cls, plan , order):
        number, payment_record = mg_OrderServer.pay(
            order.mg_order_id,
            plan.plan_amount,
            "saobei",
            ''
        )
        plan.update(payment_record_id = payment_record.id)
        url = pay_middleware.pay_order(
            "saobei",
            number,
            plan.plan_amount,
            'PC',
            ''
        )
        if url:
            plan.update(status = PlanStatus.PAYING)
        else:
            raise BusinessError('获取付款码失败')
        return url

    @classmethod
    def pay(cls, order, pay_type, trade_type = 'APP', openid = ''):
        number, payment_record = mg_OrderServer.pay(
            order.mg_order_id,
            order.deposit,
            pay_type,
            ''
        )
        prepay_id = pay_middleware.pay_order(
            pay_type,
            number,
            order.deposit,
            trade_type = trade_type,
            openid = openid
        )
        return prepay_id

    @classmethod
    def pay_success_callback(cls, output_record_number):
        mg_order, payment_record = mg_OrderServer.pay_success_callback(
            output_record_number
        )
        order = cls.search_all(mg_order_id = mg_order.id).first()
        order.update(
            status = mg_order.status,
            last_payment_time = mg_order.payment.last_payment_time
        )
        plan_qs = OrderPlanServer.search_all(
            payment_record_id = payment_record.id
        )
        if plan_qs.count() > 0:
            plan = plan_qs[0]
            plan.update(status = PlanStatus.PAID)

    @classmethod
    def pay_fail_callback(cls, output_record_number):
        mg_OrderServer.pay_fail_callback(output_record_number)

    @classmethod
    def delivery(cls, order_item, despatch_id):
        mg_order = mg_OrderServer.get(
            order_item.order.mg_order_id, is_hung = True
        )
        if mg_order.status != OrderStatus.PAYMENT_FINISHED:
            raise BusinessError('订单状态异常')
        delivery_snapshoot = None
        for snapshoot in mg_order.requirement.snapshoot_list:
            if snapshoot.id == order_item.merchandise_snapshoot_id:
                delivery_snapshoot = snapshoot
        delivery_record = mg_OrderServer.delivery(
            mg_order.id,
            delivery_snapshoot.despatch_type,  # 发货方式
            despatch_id,
            "",
            {delivery_snapshoot.id:1},
            **{}
        )
        if delivery_record:
            order_item.order.update(
                status = OrderStatus.DELIVERY_FINISHED
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

    '''
    @classmethod
    def create_beifen(cls, order_item, agent):
        number = 'Sn_200' + str(int(time.time())) + str(random.randint(10000, 99999))
        mg_order = mg_OrderServer.get(order_item.order.mg_order_id)
        mg_OrderServer.hung_snapshoot([order_item])
        contract_img_url = image_middleware.get_contract(
            number,
            agent.name,
            agent.official_seal,
            mg_order.invoice.name,
            mg_order.invoice.identification,
            mg_order.invoice.phone,
            order_item.snapshoot.brand_name,
            order_item.snapshoot.production_name,
            order_item.school_name,
            order_item.major_name,
            str(mg_order.strike_price / 100)
        )
        create_info = {
            'name': mg_order.invoice.name,
            'phone': mg_order.invoice.phone,
            'identification': mg_order.invoice.identification,
            'email': '',
            'number': number,
            'agent_customer_id': order_item.order.agent_customer_id,
            'person_id': order_item.order.person_id,
            'order_id':order_item.order.id,
            'company_id': order_item.order.company_id,
            'order_item_id': order_item.id,
            'agent_id': agent.id,
            'img_url': json.dumps(contract_img_url)
        }
        contract = Contract.create(**create_info)

        return contract
    '''

    @classmethod
    def create(cls, order_item, agent, template, contract_info_list):
        contract_qs = cls.search_all(order_item_id = order_item.id)
        if contract_qs.count() > 0:
            raise BusinessError("请不要重复生成订单")
        mg_order = mg_OrderServer.get(order_item.order.mg_order_id)
        contract_info_mapping = {}
        for contract_info in contract_info_list:
            contract_info_mapping[contract_info["template_param_id"]] = \
                                        contract_info["value"]
        param_list = []
        content_param_list = []
        for template_param in template.param_list:
            template_param.param = json.loads(template_param.content)
            if template_param.id in contract_info_mapping:
                template_param.value = contract_info_mapping[template_param.id]
                param_list.append(template_param)
                content_param_list.append({
                    "template_param_id":template_param.id,
                    "name":template_param.param["name"],
                    "key_type":template_param.param["key_type"],
                    "value":template_param.value
                })
            elif "system" in template_param.param["name_key"]:
                template_param.value = ""
                param_list.append(template_param)
        contract_img_url = contract_middleware.generate_order_contract_img(template, param_list)

        create_info = {
            'name': mg_order.invoice.name,
            'phone': mg_order.invoice.phone,
            'identification': mg_order.invoice.identification,
            'email': '',
            'agent_customer_id': order_item.order.agent_customer_id,
            'person_id': order_item.order.person_id,
            'order_id':order_item.order.id,
            'company_id': order_item.order.company_id,
            'order_item_id': order_item.id,
            'agent_id': agent.id,
            'img_url': json.dumps(contract_img_url),
            'template_id':template.id,
            'content':json.dumps(content_param_list)
        }
        contract = Contract.create(**create_info)
        return contract

    @classmethod
    def update(cls, contract, template, contract_info_list):
        contract_info_mapping = {}
        for contract_info in contract_info_list:
            contract_info_mapping[contract_info["template_param_id"]] = \
                                        contract_info["value"]
        param_list = []
        content_param_list = []
        for template_param in template.param_list:
            template_param.param = json.loads(template_param.content)
            if template_param.id in contract_info_mapping:
                template_param.value = contract_info_mapping[template_param.id]
                param_list.append(template_param)
                content_param_list.append({
                    "template_param_id":template_param.id,
                    "name":template_param.param["name"],
                    "key_type":template_param.param["key_type"],
                    "value":template_param.value
                })
            elif "system" in template_param.param["name_key"]:
                template_param.value = ""
                param_list.append(template_param)
        contract_img_url = contract_middleware.generate_order_contract_img(template, param_list)

        update_info = {
            'img_url': json.dumps(contract_img_url),
            'content':json.dumps(content_param_list)
        }
        contract.update(**update_info)
        return contract

    @classmethod
    def autograph(cls, contract, template, autograph_img, email):
        param_list = []
        for template_param in template.param_list:
            template_param.param = json.loads(template_param.content)
            if template_param.param["actual_value_source"] == ValueSource.CUSTOMER:
                if template_param.param["name_key"] == "autograph":
                    template_param.value = autograph_img
                    param_list.append(template_param)
        contract_url, contract_img_url = contract_middleware.autograph(contract, param_list)
        contract.update(**{
            'email': email,
            'autograph': autograph_img,
            'url': json.dumps([contract_url]),
            'img_url': json.dumps(contract_img_url)
        })
        mg_OrderServer.finish(
            contract.order_item.order.mg_order_id
        )
        contract.order_item.order.update(
            status = OrderStatus.ORDER_FINISHED
        )
        contract.update(status = ContractStatus.SIGNED)

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

    @classmethod
    def send_email(cls, contract_id):
        contract = cls.get(contract_id)
        if len(json.loads(contract.url)) <= 0:
            raise BusinessError('合同尚未签署')
        '''
        pdf_path = "{a}{b}".format(
            a = config_middleware.get_value("common", "domain"),
            b = json.loads(contract.url)[0]
        )
        '''
        pdf_path = json.loads(contract.url)[0]
        try:
            email_middleware.send_email(
                [contract.email],
                '教育合同',
                '教育合同',
                pdf_path
            )
        except Exception as e:
            raise BusinessError('发送失败')
        contract.update(send_email_number = F("send_email_number") + 1)
        return True

    @classmethod
    def hung_contract_byitem(cls, item_list):
        item_mapping = {}
        for item in item_list:
            item.contract = None
            item_mapping[item.id] = item
        contract_qs = cls.search_all(order_item_id__in = item_mapping.keys())
        for contract in contract_qs:
            if contract.order_item_id in item_mapping:
                item_mapping[contract.order_item_id].contract = contract
        return item_list


class OrderPlanServer(BaseManager):

    @classmethod
    def generate_number(cls):
        return "PL" + str(time.time()).replace('.', '')

    @classmethod
    def create(cls, **info):
        info.update({
            "number":cls.generate_number()
        })
        plan = Plan.create(**info)
        if plan is None:
            raise BusinessError("回款计划添加失败")
        return plan

    @classmethod
    def batch_create(cls, order, staff_id, plan_list):
        create_list = []
        for obj in plan_list:
            create_list.append(Plan(
                unique_number = Plan.generate_unique_number(),
                order = order,
                number = cls.generate_number(),
                staff_id = staff_id,
                plan_time = obj["plan_time"],
                plan_amount = obj["plan_amount"],
            ))
        Plan.objects.bulk_create(create_list)

    @classmethod
    def check_money(cls, surplus_money, order, plan_amount, plan = None):
        plan_surplus_money = 0
        total_surplus_money = cls.search_all(
            order = order,
            status__in = [PlanStatus.WAIT_PAY, PlanStatus.PAYING],
        )
        if plan is not None:
            total_surplus_money = total_surplus_money.exclude(id = plan.id)
        total_surplus_money = total_surplus_money.\
                              aggregate(total_money = Sum("plan_amount"))
        if total_surplus_money["total_money"] is not None:
            plan_surplus_money = total_surplus_money["total_money"]
        if plan_surplus_money + plan_amount > surplus_money:
            raise BusinessError("回款计划金额大于实际待付款金额")
        return True

    @classmethod
    def search_all(cls, **search_info):
        plan_qs = Plan.search(**search_info)
        return plan_qs

    @classmethod
    def get(cls, plan_id):
        plan = Plan.get_byid(plan_id)
        if plan is None:
            raise BusinessError("此回款计划不存在")
        return plan

    @classmethod
    def remove(cls, plan_id):
        plan = Plan.get_byid(plan_id)
        if plan.status == PlanStatus.PAID:
            raise BusinessError("已回款计划禁止删除")
        plan.delete()
        return True

    @classmethod
    def update(cls, plan, **update_info):
        plan.update(**update_info)
        return plan
