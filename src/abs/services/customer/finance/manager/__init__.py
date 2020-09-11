# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.middleground.business.transaction.manager import TransactionServer
from abs.middleground.business.person.manager import PersonServer
from abs.middleground.business.transaction.utils.constant import \
        BusinessTypes, TransactionStatus, PayTypes
from abs.services.customer.personal.manager import CustomerServer
from abs.services.customer.finance.models import CustomerBalanceRecord
from abs.middleware.extend.yunaccount import yunaccount_extend
from abs.middleware.pay import pay_middleware


class CustomerFinanceServer(BaseManager):

    @classmethod
    def get_balance(cls, customer_id):
        customer = CustomerServer.get(customer_id)
        balance = TransactionServer.get_person_balance(customer.person_id)
        return balance

    @classmethod
    def withdraw(cls, customer_id, amount, pay_type, remark, bankcard_id):
        customer = CustomerServer.get(customer_id)
        cls.check_withdraw(customer, amount, pay_type, bankcard_id)

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
        flag = False
        if pay_type == PayTypes.BANK:
            bankcard = PersonServer.get_bankcard(bankcard_id)
            if bankcard:
                flag, result = yunaccount_extend.transfers(
                    amount,
                    bankcard,
                    output_record.number
                )

        if not flag:
            TransactionServer.failure_output_record_bynumber(
                output_record.number
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
            status=TransactionStatus.TRANSACTION_DEALING
        )

        prepay_id = pay_middleware.top_up(
            pay_type,
            input_record.number,
            amount
        )

        if not prepay_id:
            TransactionServer.update_inputrecord(
                input_record_id=input_record.id,
                status=TransactionStatus.ACCOUNT_FAIL,
            )
            raise BusinessError('调用支付失败')

        return prepay_id

    @classmethod
    def top_up_notify(cls, number, pay_time, transaction_id, price):
        input_record = TransactionServer.get_input_record_bynumber(number)
        if not input_record:
            raise BusinessError('付款单不存在')
        if input_record.amount != int(price):
            raise BusinessError('金额不正确')
        if input_record:
            # 支付到账
            TransactionServer.update_inputrecord(
                input_record_id=input_record.id,
                status=TransactionStatus.ACCOUNT_FINISH,
            )
            return True
        raise BusinessError('单号不存在')

    @classmethod
    def withdraw_success_notify(cls, record_number):
        record = TransactionServer.get_output_record_bynumber(record_number)
        if record:
            record.update(
                status=TransactionStatus.ACCOUNT_FINISH
            )

    @classmethod
    def withdraw_wait_notify(cls, record_number):
        # todo 待打款暂停处理逻辑
        record = TransactionServer.get_output_record_bynumber(
            record_number
        )
        return record

    @classmethod
    def withdraw_fail_notify(cls, record_number):
        record = TransactionServer.get_output_record_bynumber(
            record_number
        )
        if record:
            record.update(
                status=TransactionStatus.ACCOUNT_FAIL
            )

    @classmethod
    def check_withdraw(cls, customer, amount, pay_type, bankcard_id):
        if pay_type != PayTypes.BANK:
            raise BusinessError('此提现渠道暂未开放！')
        if amount <= 0:
            raise BusinessError('提现金额异常！')
        bankcard = PersonServer.get_bankcard(bankcard_id)
        if bankcard.person.id != customer.person_id:
            raise BusinessError('提现银行卡与用户不匹配！')
        balance = TransactionServer.get_person_balance(customer.person_id)
        if amount > balance:
            raise BusinessError('账号余额不足！')
