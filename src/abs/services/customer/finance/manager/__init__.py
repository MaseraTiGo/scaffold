# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.middleground.business.transaction.manager import TransactionServer
from abs.middleground.business.transaction.utils.constant import \
        BusinessTypes, TransactionStatus
from abs.services.customer.personal.manager import CustomerServer
from abs.services.customer.finance.models import CustomerBalanceRecord


class CustomerFinanceServer(BaseManager):

    @classmethod
    def get_balance(cls, customer_id):
        customer = CustomerServer.get(customer_id)
        balance = TransactionServer.get_person_balance(customer.person_id)
        return balance

    @classmethod
    def withdraw(cls, customer_id, amount, pay_type, remark):
        customer = CustomerServer.get(customer_id)
        balance = TransactionServer.get_person_balance(customer.person_id)
        if amount > balance:
            raise BusinessError('账号余额不足！')

        expense_amount = 0 - amount
        # 1. 创建余额凭证
        balance_record = CustomerBalanceRecord.create(
            amount=expense_amount,
            remark=remark,
            pay_type=pay_type,
            customer_id=customer_id,
        )

        # 2. 生成出账单
        output_record = TransactionServer.generate_p2c_outputrecord(
            person_id=customer.person_id,
            company_id=EnterpriseServer.get_main_company().id,
            amount=balance_record.amount,
            pay_type=balance_record.pay_type,
            remark=balance_record.remark,
            business_type=BusinessTypes.BALANCE,
            business_id=balance_record.id,
        )

        # 3. 绑定出账单到余额凭证中
        balance_record.update(
            output_record_id=output_record.id,
        )
        return balance_record

    @classmethod
    def top_up(cls, customer_id, amount, pay_type, remark):
        customer = CustomerServer.get(customer_id)

        # 1. 生成入账单
        input_record = TransactionServer.generate_p2c_inputrecord(
            person_id=customer.person_id,
            company_id=EnterpriseServer.get_main_company().id,
            amount=amount,
            pay_type=pay_type,
            remark=remark,
            business_type=BusinessTypes.BALANCE,
        )

        # 2. 创建余额凭证
        balance_record = CustomerBalanceRecord.create(
            amount=input_record.amount,
            remark=input_record.remark,
            pay_type=input_record.pay_type,
            customer_id=customer.id,
            input_record_id=input_record.id,
        )

        # 3. 绑定余额凭证到入账单
        TransactionServer.update_inputrecord(
            input_record_id=input_record.id,
            business_id=balance_record.id,
        )

        # 4. 模拟支付到账
        TransactionServer.update_inputrecord(
            input_record_id=input_record.id,
            status=TransactionStatus.ACCOUNT_FINISH,
        )
        return balance_record
