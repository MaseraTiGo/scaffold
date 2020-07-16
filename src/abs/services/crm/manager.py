# coding=UTF-8


import hashlib
import random
import collections
from django.db.models import Q

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.service.base import BaseServer
from abs.middleware.token import TokenManager
from model.common.model_account_base import StatusTypes
from model.store.model_customer import Customer, CustomerAccount, CustomerAddress, \
                CustomerBankCard, CustomerTransactionRecord, CustomerTransactionOutputRecord, \
                    CustomerTransactionInputRecord, CustomerBalanceRecord, BusinessTypes, \
                        TransactionStatus, PayTypes


class CustomerServer(BaseServer):

    @classmethod
    def get(cls, customer):
        return cls.get_byid(customer.id)

    @classmethod
    def get_byid(cls, customer_id):
        customer = Customer.get_byid(customer_id)
        return customer

    @classmethod
    def search(cls, current_page, **search_info):
        customer_qs = Customer.search(**search_info)
        customer_qs.order_by('-create_time')
        return Splitor(current_page, customer_qs)

    @classmethod
    def generate(cls, customer_info):
        customer = Customer.create(**customer_info)
        return customer

    @classmethod
    def update(cls, customer_id, **update_info):
        customer = cls.get_byid(customer_id)
        customer.update(**update_info)
        return customer

    @classmethod
    def add_address(cls, customer_id, **address_info):
        customer = cls.get_byid(customer_id)
        address = CustomerAddress.create(customer = customer, **address_info)
        return address

    @classmethod
    def get_address(cls, address_id):
        address = CustomerAddress.get_byid(address_id)
        return address

    @classmethod
    def get_all_address(cls, customer_id):
        address_qs = CustomerAddress.search(customer = customer_id)
        return address_qs
    
    @classmethod
    def remove_address(cls, address_id):
        return cls.get_address(address_id).delete()

    @classmethod
    def update_address(cls, address_id, **address_info):
        address = cls.get_address(address_id)
        address.update(**address_info)
        return address

    @classmethod
    def add_bankcard(cls, customer_id, bank_number, **bankcard_info):
        customer = cls.get_byid(customer_id)

        # todo: add card to verify
        bank_list = (
            ('中国工商银行', "ICBC"),
            ('中国邮政储蓄银行', "PSBC"),
            ('中国农业银行', "ABC"),
            ('中国银行', "BOC"),
            ('中国建设银行', "CCB"),
            ('中国交通银行', "COMM"),
            ('招商银行', "CMB"),
        )
        bank_name, bank_code = random.choice(bank_list)

        bankcard = CustomerBankCard.create(customer = customer, bank_name = bank_name, bank_code =
                                           bank_code, bank_number = bank_number, **bankcard_info)
        return bankcard

    @classmethod
    def get_bankcard(cls, bankcard_id):
        bankcard = CustomerBankCard.get_byid(bankcard_id)
        return bankcard

    @classmethod
    def get_all_bankcard(cls, customer_id):
        bankcard = CustomerBankCard.search(customer = customer_id)
        return bankcard

    @classmethod
    def remove_bankcard(cls, bankcard_id):
        return cls.get_bankcard(bankcard_id).delete()


class CustomerAccountServer(BaseServer):

    @classmethod
    def register(cls, phone, password, code):
        customer_qs = Customer.search(phone = phone)
        customer_account_qs = CustomerAccount.search(username = phone)
        if customer_qs.count() > 0 or customer_account_qs.count() > 0:
            raise BusinessError('账号或密码已存在！')

        customer = Customer.create(phone = phone)
        customer_account = CustomerAccount.create(customer = customer, username = phone, \
                                                  password = password, status = StatusTypes.ENABLE)
        token = TokenManager.generate_token('user', customer.id)
        return token

    @classmethod
    def renew_token(cls, auth_str, renew_str):
        return TokenManager.renew_token(auth_str, renew_str)

    @classmethod
    def login(cls, username, password):
        is_exsited, account = CustomerAccount.is_exsited(username, password)
        if is_exsited:
            token = TokenManager.generate_token('user', account.customer.id)
            return token
        raise BusinessError('账号或密码不存在！')

    @classmethod
    def modify_password(cls, customer_id, old_password, new_password):
        account = CustomerAccount.get_account_bycustomer(customer_id)
        if account.password != old_password:
            raise BusinessError('老密码不正确，请重试！')
        account.update(password = new_password)
        return True

    @classmethod
    def forget_password(cls, phone, code, new_password):
        # todo: 需要获取验证码
        if code  != "123456":
            raise BusinessError('验证码错误，请重新输入！')
        account = CustomerAccount.get_byphone(phone)
        if account is None:
            raise BusinessError('账户不存在！')

        account.update(password = new_password)
        token = TokenManager.generate_token('user', account.customer.id)
        return token

    @classmethod
    def logout(cls, customer):
        pass

    @classmethod
    def get_phone_verification_code(cls, phone_number):
        return "123456"

    @classmethod
    def get_image_verification_code(cls):
        return "654321"


class CustomerFinanceServer(BaseServer):

    @classmethod
    def search_transaction_record(cls, current_page, **search_info):
        transaction_record_qs = CustomerTransactionRecord.search(**search_info)
        transaction_record_qs.order_by('-create_time')
        return Splitor(current_page, transaction_record_qs)

    @classmethod
    def statistics_customer_bymonth(cls, customer_id):
        customer = CustomerServer.get_byid(customer_id)
        transaction_record_qs = CustomerTransactionRecord.\
                search(customer = customer).order_by("-create_time")
        statistics_result = collections.OrderedDict()
        for transaction in transaction_record_qs:
            key = (transaction.create_time.year, transaction.create_time.month)
            if key not in statistics_result:
                statistics_result[key] = [0, 0]
            if transaction.input_record_id:
                statistics_result[key][0] += transaction.amount
            if transaction.output_record_id:
                statistics_result[key][1] += transaction.amount

        result = [[key[0], key[1], result[0], result[1]] for key, result in statistics_result.items()]
        return result

    @classmethod
    def get_balance(cls, customer_id):
        customer = CustomerServer.get_byid(customer_id)
        balance = CustomerBalanceRecord.get_balance(customer)
        return balance

    @classmethod
    def withdraw(cls, customer_id, amount, pay_type, remark):
        customer = CustomerServer.get_byid(customer_id)
        balance = cls.get_balance(customer_id)
        if amount > balance:
            raise BusinessError('账号余额不足！')

        expense_amount = 0 - amount
        # 1. 创建余额凭证
        balance_record = CustomerBalanceRecord.create(
            amount = expense_amount,
            remark = remark,
            pay_type = pay_type,
            customer = customer,
        )

        # 2. 生成出账单
        output_record = CustomerTransactionOutputRecord.create(
            amount = balance_record.amount,
            pay_type = balance_record.pay_type,
            remark = balance_record.remark,
            customer = customer,
            business_type = BusinessTypes.BALANCE,
            business_id = balance_record.id,
        )

        # 3. 绑定出账单到余额凭证中
        balance_record.update(
            output_record = output_record,
        )
        return balance_record

    @classmethod
    def top_up(cls, customer_id, amount, pay_type, remark):
        customer = CustomerServer.get_byid(customer_id)

        # 1. 生成入账单
        input_record = CustomerTransactionInputRecord.create(
            amount = amount,
            pay_type = pay_type,
            remark = remark,
            customer = customer,
            business_type = BusinessTypes.BALANCE,
        )

        # 2. 创建余额凭证
        balance_record = CustomerBalanceRecord.create(
            amount = input_record.amount,
            remark = input_record.remark,
            pay_type = input_record.pay_type,
            customer = input_record.customer,
            input_record = input_record,
        )

        # 3. 绑定余额凭证到入账单
        input_record.update(
            business_id = balance_record.id,
        )

        # 4. 模拟支付到账
        input_record.update(
            status = TransactionStatus.ACCOUNT_FINISH,
        )
        return balance_record

    @classmethod
    def get_transacation_detail(cls, transaction_id):
        transaction =  CustomerTransactionRecord.get_byid(transaction_id)
        if transaction.input_record_id:
            transaction.record = CustomerTransactionInputRecord.get_byid(transaction.input_record_id)
        if transaction.output_record_id:
            transaction.record = CustomerTransactionOutputRecord.get_byid(transaction.output_record_id)
        return transaction
