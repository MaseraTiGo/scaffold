# coding=UTF-8


from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator
from support.common.generator.field.normal import *
from support.common.generator.field.model import *
from support.common.generator.helper import CustomerGenerator
from model.common.model_user_base import UserCertification
from model.store.model_customer import CustomerTransactionOutputRecord,\
        CustomerTransactionInputRecord, CustomerTransactionRecord, CustomerBalanceRecord,\
            BusinessTypes


class CustomerBalanceGenerator(BaseGenerator):

    def __init__(self, balance_infos):
        super(CustomerBalanceGenerator, self).__init__()
        self._balance_infos = self.init(balance_infos)

    def get_create_list(self, result_mapping):
        customer_list = result_mapping.get(CustomerGenerator.get_key())
        balance_list = []
        for customer in customer_list:
            for balance_info in self._balance_infos:
                balance_info.update({
                    'customer': customer,
                })
                balance_list.append(balance_info)
        return balance_list

    def create(self, balance_info, result_mapping):
        is_input = balance_info.pop("is_input")
        balance = CustomerBalanceRecord.create(**balance_info)
        if is_input:
            input_record = CustomerTransactionInputRecord.create(
                amount = balance.amount,
                pay_type = balance.pay_type,
                remark = balance.remark,
                business_type = BusinessTypes.BALANCE,
                business_id = balance.id,
                customer = balance.customer,
                create_time = balance.create_time,
            )
            input_record.update(status = TransactionStatusConstant().generate())
            balance.update(input_record = input_record)
        else:
            output_record = CustomerTransactionOutputRecord.create(
                amount = balance.amount,
                pay_type = balance.pay_type,
                remark = balance.remark,
                business_type = BusinessTypes.BALANCE,
                business_id = balance.id,
                customer = balance.customer,
                create_time = balance.create_time,
            )
            output_record.update(status = TransactionStatusConstant().generate())
            balance.update(output_record = output_record)
        return balance

    def delete(self):
        print('======================>>> delete customer <======================')
        return None
