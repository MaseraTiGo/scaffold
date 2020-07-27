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
from abs.middleware.wechat import wechat_middleware
from abs.middleware.extend.yunaccount import yunaccount_extend
from abs.middleware.alipay import alipay_middleware


class CustomerFinanceServer(BaseManager):

    @classmethod
    def get_balance(cls, customer_id):
        customer = CustomerServer.get(customer_id)
        balance = TransactionServer.get_person_balance(customer.person_id)
        return balance

    @classmethod
    def withdraw(cls, customer_id, amount, pay_type, remark, bankcard_id):
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
            status=TransactionStatus.TRANSACTION_DEALING
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
            TransactionServer.update_outputrecord(
                output_record_id=output_record.id,
                status=TransactionStatus.ACCOUNT_FAIL
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

        prepay_id = ''
        if pay_type == PayTypes.WECHAT:
            result = wechat_middleware.unifiedorder_app(
                input_record.number,
                input_record.amount,
                '充值'
            )
            if result:
                prepay_id = result['prepay_id']
        elif pay_type == PayTypes.ALIPAY:
            prepay_id = alipay_middleware.get_app_top_up_info(input_record)

        if not prepay_id:
            TransactionServer.update_inputrecord(
                input_record_id=input_record.id,
                status=TransactionStatus.ACCOUNT_FAIL,
            )
            raise BusinessError('调用支付失败')

        return prepay_id

    @classmethod
    def parse_pay_info(cls, prepay_id, pay_type):
        pay_info = {
            'timestamp': '',
            'prepayid': '',
            'noncestr': '',
            'sign': ''
        }
        if pay_type == PayTypes.WECHAT:
            pay_info = wechat_middleware.get_app_sign(prepay_id)
            pay_info.update({
                'timestamp': pay_info.get('timestamp'),
                'prepayid': pay_info.get('prepayid'),
                'noncestr': pay_info.get('noncestr'),
                'sign': pay_info.get('sign')
            })
        elif pay_type == PayTypes.ALIPAY:
            pay_info.update({
                'prepayid': prepay_id
            })
        return pay_info

    @classmethod
    def top_up_notify(cls, number, pay_time, transaction_id, price):
        input_record = TransactionServer.get_input_record_bynumber(number)
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
            record.update(status=TransactionStatus.ACCOUNT_FINISH)

    @classmethod
    def withdraw_wait_notify(cls, record_number):
        # todo 待打款暂停处理逻辑
        record = TransactionServer.get_output_record_bynumber(record_number)
        pass

    @classmethod
    def withdraw_fail_notify(cls, record_number):
        record = TransactionServer.get_output_record_bynumber(record_number)
        if record:
            record.update(status=TransactionStatus.ACCOUNT_FAIL)
