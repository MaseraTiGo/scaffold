# coding=UTF-8


from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator
from support.common.generator.field.model import TransactionStatusConstant
from support.common.generator.helper import CustomerGenerator,\
        EnterpriseGenerator
from abs.middleground.business.transaction.utils.constant import \
        BusinessTypes, OwnTypes
from abs.middleground.business.transaction.store import \
        TransactionInputRecord, TransactionOutputRecord
from abs.services.customer.finance.store import CustomerBalanceRecord


class CustomerBalanceGenerator(BaseGenerator):

    def __init__(self, balance_infos):
        super(CustomerBalanceGenerator, self).__init__()
        self._balance_infos = self.init(balance_infos)

    def get_create_list(self, result_mapping):
        customer_list = result_mapping.get(CustomerGenerator.get_key())
        enterprise_list = result_mapping.get(EnterpriseGenerator.get_key())
        balance_list = []
        for enterprise in enterprise_list:
            for customer in customer_list:
                for balance_info in self._balance_infos:
                    balance_info.update({
                        'customer_id': customer.id,
                        'person_id': customer.person_id,
                        'enterprise_id': enterprise.id,
                    })
                    balance_list.append(balance_info)
        return balance_list

    def create(self, balance_info, result_mapping):
        is_input = balance_info.pop("is_input")
        person_id = balance_info.pop("person_id")
        company_id = balance_info.pop("enterprise_id")
        balance = CustomerBalanceRecord.create(**balance_info)
        if is_input:
            input_record = TransactionInputRecord.create(
                amount=balance.amount,
                pay_type=balance.pay_type,
                remark=balance.remark,
                business_type=BusinessTypes.BALANCE,
                business_id=balance.id,
                own_type=OwnTypes.PERSON,
                own_id=person_id,
                trader_type=OwnTypes.COMPANY,
                trader_id=company_id,
                create_time=balance.create_time,
            )
            input_record.update(status=TransactionStatusConstant().generate())
            balance.update(input_record_id=input_record.id)
        else:
            output_record = TransactionOutputRecord.create(
                amount=balance.amount,
                pay_type=balance.pay_type,
                remark=balance.remark,
                business_type=BusinessTypes.BALANCE,
                business_id=balance.id,
                own_type=OwnTypes.PERSON,
                own_id=person_id,
                trader_type=OwnTypes.COMPANY,
                trader_id=company_id,
                create_time=balance.create_time,
            )
            output_record.update(status=TransactionStatusConstant().generate())
            balance.update(output_record_id=output_record.id)
        return balance

    def delete(self):
        logger.info('============>>> delete customer <=================')
        return None
