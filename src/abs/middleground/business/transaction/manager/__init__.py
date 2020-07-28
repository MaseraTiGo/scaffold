# coding=UTF-8

import collections

from infrastructure.utils.common.split_page import Splitor
from abs.common.model import Sum
from abs.common.manager import BaseManager
from abs.middleground.business.transaction.utils.constant import OwnTypes,\
        BusinessTypes
from abs.middleground.business.transaction.models import TransactionRecord,\
        TransactionInputRecord, TransactionOutputRecord


class TransactionServer(BaseManager):

    @classmethod
    def search_transaction_record(cls, current_page, **search_info):
        transaction_record_qs = TransactionRecord.search(**search_info)
        transaction_record_qs.order_by('-create_time')
        return Splitor(current_page, transaction_record_qs)

    @classmethod
    def search_person_transaction(cls, current_page, person_id, **search_info):
        transaction_record_qs = TransactionRecord.search(
            own_type=OwnTypes.PERSON,
            own_id=person_id,
            **search_info
        )
        transaction_record_qs.order_by('-create_time')
        return Splitor(current_page, transaction_record_qs)

    @classmethod
    def generate_p2c_outputrecord(cls, person_id, company_id, **output_record):
        output_record = cls.generate_outputrecord(
            own_type=OwnTypes.PERSON,
            own_id=person_id,
            trader_type=OwnTypes.COMPANY,
            trader_id=company_id,
            **output_record
        )
        return output_record

    @classmethod
    def generate_outputrecord(
        cls,
        own_type,
        own_id,
        trader_type,
        trader_id,
        **output_record
    ):
        output_record = TransactionOutputRecord.create(
            own_type=own_type,
            own_id=own_id,
            trader_type=trader_type,
            trader_id=trader_id,
            **output_record
        )
        return output_record

    @classmethod
    def generate_p2c_inputrecord(cls, person_id, company_id, **input_record):
        input_record = TransactionInputRecord.create(
            own_type=OwnTypes.PERSON,
            own_id=person_id,
            trader_type=OwnTypes.COMPANY,
            trader_id=company_id,
            **input_record
        )
        return input_record

    @classmethod
    def update_inputrecord(cls, input_record_id, **input_infos):
        input_record = TransactionInputRecord.get_byid(input_record_id)
        input_record.update(**input_infos)
        return input_record

    @classmethod
    def update_outputrecord(cls, output_record_id, **output_infos):
        output_record = TransactionOutputRecord.get_byid(output_record_id)
        output_record.update(**output_infos)
        return output_record

    @classmethod
    def statistics_person_bymonth(cls, person_id):
        transaction_record_qs = TransactionRecord.search(
            own_type=OwnTypes.PERSON,
            own_id=person_id
        ).order_by("-create_time")
        statistics_result = collections.OrderedDict()
        for transaction in transaction_record_qs:
            key = (transaction.create_time.year, transaction.create_time.month)
            if key not in statistics_result:
                statistics_result[key] = [0, 0]
            if transaction.input_record_id:
                statistics_result[key][0] += transaction.amount
            if transaction.output_record_id:
                statistics_result[key][1] += transaction.amount

        result = [
            [key[0], key[1], result[0], result[1]]
            for key, result in statistics_result.items()
        ]
        return result

    @classmethod
    def get_person_balance(cls, person_id):
        result = TransactionRecord.search(
            own_type=OwnTypes.PERSON,
            own_id=person_id,
            business_type=BusinessTypes.BALANCE
        ).aggregate(total=Sum('amount'))
        if result['total'] is None:
            return 0
        return result['total']

    @classmethod
    def get_transacation_detail(cls, transaction_id):
        transaction = TransactionRecord.get_byid(transaction_id)
        if transaction.input_record_id:
            transaction.record = TransactionInputRecord.get_byid(
                transaction.input_record_id
            )
        if transaction.output_record_id:
            transaction.record = TransactionOutputRecord.get_byid(
                transaction.output_record_id
            )
        return transaction

    @classmethod
    def get_input_record_bynumber(cls, number):
        return TransactionInputRecord.search(number=number).first()

    @classmethod
    def get_output_record_bynumber(cls, number):
        return TransactionOutputRecord.search(number=number).first()
