# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.transaction.manager import TransactionServer
from abs.middleground.business.transaction.utils.constant import \
        BusinessTypes
from abs.middleground.business.order.utils.constant import OrderStatus
from abs.middleground.business.order.models import Requirement, \
        MerchandiseSnapShoot, Payment, PaymentRecord, Invoice, \
        DeliveryRecord, DeliveryRecordList, Order


class OrderServer(BaseManager):

    @classmethod
    def _hung_requirement(cls, order_list):
        requirement_mapping = {}
        for order in order_list:
            requirement_mapping.update({
                order.requirement.id: order.requirement
            })
            order.requirement.snapshoot_list = []

        for snapshoot in MerchandiseSnapShoot.query().filter(
            requirement_id__in=requirement_mapping.keys()
        ):
            requirement = requirement_mapping[snapshoot.requirement_id]
            requirement.snapshoot_list.append(snapshoot)

    @classmethod
    def _hung_payment(cls, order_list):
        payment_mapping = {}
        for order in order_list:
            payment_mapping.update({
                order.payment.id: order.payment
            })
            order.payment.payment_list = []

        for record in PaymentRecord.query().filter(
            payment_id__in=payment_mapping.keys()
        ):
            payment = payment_mapping[record.payment_id]
            payment.payment_list.append(record)

    @classmethod
    def _hung_delivery_record(cls, order_list):
        invoice_mapping = {}
        for order in order_list:
            invoice_mapping.update({
                order.invoice.id: order.invoice
            })
            order.invoice.delivery_list = []

        for delivery in DeliveryRecord.query().filter(
            invoice_id__in=invoice_mapping.keys()
        ):
            invoice = invoice_mapping[delivery.invoice_id]
            invoice.delivery_list.append(delivery)

    @classmethod
    def get(cls, order_id, is_hung=False):
        order = Order.get_byid(order_id)
        if order is None:
            raise BusinessError("订单不存在")
        if is_hung:
            cls._hung_requirement([order])
            cls._hung_payment([order])
            cls._hung_delivery_record([order])
        return order

    @classmethod
    def search(cls, current_page, is_hung=False, **search_info):
        order_qs = Order.query().filter(
            **search_info
        )
        spliter = Splitor(current_page, order_qs)
        if is_hung:
            cls._hung_requirement(spliter.get_list())
            cls._hung_payment(spliter.get_list())
            cls._hung_delivery_record(spliter.get_list())
        return spliter

    @classmethod
    def _generate_requirement(cls, specification_list, strike_price):
        requirement = Requirement.create(
            sale_price=strike_price
        )
        snapshoot_list = [
            MerchandiseSnapShoot(
                production_id=specification.merchandise.production_id,
                merchandise_id=specification.merchandise.id,
                despatch_type=specification.merchandise.despatch_type,
                specification_id=specification.id,
                title=specification.merchandise.title,
                show_image=specification.show_image,
                sale_price=specification.sale_price,
                production_name=specification.production.name,
                brand_name=specification.production.brand.name,
                count=specification.order_count,
                total_price=specification.total_price,
                requirement=requirement,
                unique_number=MerchandiseSnapShoot.generate_unique_number(),
                remark=','.join([
                    (sv.category + '|' + sv.attribute)
                    for sv in specification.specification_value_list
                ]),
            )
            for specification in specification_list
        ]
        MerchandiseSnapShoot.objects.bulk_create(snapshoot_list)
        return requirement

    @classmethod
    def place(
        cls,
        specification_list,
        strike_price,
        remark,
        launch_type,
        launch_id,
        server_type,
        server_id,
        **invoice_baseinfos
    ):
        """
        下单接口，注意该接口用时需要进行转换，将
        specification对象挂载 order_count, total_price, production属性
        strike_price 是总成交价
        """
        requirement = cls._generate_requirement(
            specification_list,
            strike_price
        )
        payment = Payment.create(
            actual_amount=requirement.sale_price
        )
        invoice = Invoice.create(
            requirement=requirement,
            **invoice_baseinfos
        )
        order = Order.create(
            remark=remark,
            strike_price=payment.actual_amount,
            payment=payment,
            requirement=requirement,
            invoice=invoice,
            launch_type=launch_type,
            launch_id=launch_id,
            server_type=server_type,
            server_id=server_id,
        )
        return order

    @classmethod
    def pay(cls, order_id, amount, pay_type, remark):
        order = cls.get(order_id)
        expense_amount = 0 - amount
        # 1. 生成支付账单
        payment_record = PaymentRecord.create(
            amount=expense_amount,
            pay_type=pay_type,
            payment=order.payment
        )

        # 2. 生成出账单
        output_record = TransactionServer.generate_outputrecord(
            own_type=order.launch_type,
            own_id=order.launch_id,
            trader_type=order.server_type,
            trader_id=order.server_id,
            amount=expense_amount,
            pay_type=pay_type,
            remark=remark,
            business_type=BusinessTypes.ORDER,
            business_id=payment_record.id,
        )

        # 3. 绑定出账单到订单凭证中
        payment_record.update(
            output_record_id=output_record.id,
        )
        return output_record.number

    @classmethod
    def pay_success_callback(cls, output_record_number):
        output_record = TransactionServer.finished_output_record_bynumber(
            output_record_number
        )
        payment_record = PaymentRecord.get_byoutputrecord(
            output_record_id=output_record.id
        )
        if payment_record is None:
            raise BusinessError("支付信息不存在")
        payment_record.update(
            status=output_record.status
        )

        payment = payment_record.payment
        amount = 0 - payment_record.amount
        payment.update(
            actual_amount=payment.actual_amount + amount,
            last_payment_amount=amount,
            last_payment_type=payment_record.pay_type,
            last_payment_time=payment_record.create_time,
        )

        order = Order.get_bypayment(payment.id)
        if order is None:
            raise BusinessError("订单信息不存在")
        order.update(
            status=OrderStatus.PAYMENT_FINISHED
        )
        return order

    @classmethod
    def pay_fail_callback(cls, output_record_number):
        output_record = TransactionServer.failure_output_record_bynumber(
            output_record_number
        )
        payment_record = PaymentRecord.get_byoutputrecord(
            output_record_id=output_record.id
        )
        if payment_record is None:
            raise BusinessError("支付信息不存在")
        payment_record.update(
            status=output_record.status
        )

    @classmethod
    def delivery(
        cls,
        order_id,
        despatch_type,
        despatch_id,
        remark,
        snapshoot_mapping,
        **invoice_baseinfos
    ):
        """
        snapshoot_mapping={
            key: 快照id，
            value: 发货数量，
        }
        """
        order = cls.get(order_id)
        order.invoice.update(
            **invoice_baseinfos
        )
        delivery_record = DeliveryRecord.create(
            despatch_type=despatch_type,
            despatch_id=despatch_id,
            remark=remark,
            invoice=order.invoice
        )
        delivery_list = [
            DeliveryRecordList(
                delivery_count=snapshoot_mapping[snapshoot.id],
                snapshoot=snapshoot,
                delivery_record=delivery_record,
                unique_number=DeliveryRecordList.generate_unique_number(),
            )
            for snapshoot in MerchandiseSnapShoot.query().filter(
                id__in=snapshoot_mapping.keys()
            )
        ]
        if len(delivery_list) == 0:
            raise BusinessError("请正确选择发货商品")
        DeliveryRecordList.objects.bulk_create(delivery_list)
        order.update(
            status=OrderStatus.DELIVERY_FINISHED
        )
        return delivery_record

    @classmethod
    def finish(cls, order_id):
        order = cls.get(order_id)
        order.update(
            status=OrderStatus.ORDER_FINISHED
        )

    @classmethod
    def close(cls, order_id):
        order = cls.get(order_id)
        order.update(
            status=OrderStatus.ORDER_CLOSED
        )

    @classmethod
    def hung_order(cls, obj_list):
        mg_order_mapping = {}
        for obj in obj_list:
            obj.mg_order = None
            mg_order_mapping[obj.mg_order_id] = obj

        mg_order_list = list(Order.query().filter(
            id__in=mg_order_mapping.keys()
        ))
        cls._hung_payment(mg_order_list)
        cls._hung_delivery_record(mg_order_list)
        for mg_order in mg_order_list:
            if mg_order.id in mg_order_mapping:
                mg_order_mapping[mg_order.id].mg_order = mg_order
        return obj_list

    @classmethod
    def hung_snapshoot(cls, obj_list):
        snapshoot_mapping = {}
        for obj in obj_list:
            obj.snapshoot = None
            snapshoot_mapping[obj.merchandise_snapshoot_id] = obj

        snapshoot_qs = MerchandiseSnapShoot.query().filter(
            id__in=snapshoot_mapping.keys()
         )
        for snapshoot in snapshoot_qs:
            if snapshoot.id in snapshoot_mapping:
                snapshoot_mapping[snapshoot.id].snapshoot = snapshoot
        return obj_list

    @classmethod
    def search_all_snapshoot(cls, **search_info):
        return MerchandiseSnapShoot.query().filter(**search_info)

    @classmethod
    def search_order_id_list(cls, **search_info):
        return list(Order.query().filter(
            **search_info
        ).values_list('id', flat=True))
