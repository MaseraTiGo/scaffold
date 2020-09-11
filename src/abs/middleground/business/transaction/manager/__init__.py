# coding=UTF-8

import collections

from infrastructure.utils.common.split_page import Splitor
from abs.common.model import Sum
from abs.common.manager import BaseManager
from abs.middleground.business.transaction.utils.constant import OwnTypes,\
        BusinessTypes, TransactionStatus
from abs.middleground.business.transaction.models import TransactionRecord,\
        TransactionInputRecord, TransactionOutputRecord


class TransactionServer(BaseManager):

    @classmethod
    def search_transaction_record(cls, current_page, **search_info):
        """
        搜索交易记录
        """
        transaction_record_qs = TransactionRecord.search(**search_info)
        transaction_record_qs.order_by('-create_time')
        return Splitor(current_page, transaction_record_qs)

    @classmethod
    def search_person_transaction(cls, current_page, person_id, **search_info):
        """
        搜索个人交易记录
        """
        result = cls.search_transaction_record(
            current_page,
            own_type=OwnTypes.PERSON,
            own_id=person_id,
            **search_info
        )
        return result

    @classmethod
    def generate_outputrecord(
        cls,
        own_type,
        own_id,
        trader_type,
        trader_id,
        **output_record
    ):
        """
        生成出账记录
        """
        output_record = TransactionOutputRecord.create(
            own_type=own_type,
            own_id=own_id,
            trader_type=trader_type,
            trader_id=trader_id,
            **output_record
        )
        return output_record

    @classmethod
    def generate_p2c_outputrecord(cls, person_id, company_id, **output_record):
        """
        生成出账记录（个人对公司）
        """
        output_record = cls.generate_outputrecord(
            own_type=OwnTypes.PERSON,
            own_id=person_id,
            trader_type=OwnTypes.COMPANY,
            trader_id=company_id,
            **output_record
        )
        return output_record

    @classmethod
    def generate_p2c_inputrecord(cls, person_id, company_id, **input_record):
        """
        生成入账记录（个人对公司）
        """
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
        """
        更新入账单
        """
        input_record = TransactionInputRecord.get_byid(input_record_id)
        input_record.update(**input_infos)
        return input_record

    @classmethod
    def update_outputrecord(cls, output_record_id, **output_infos):
        """
        更新出账单
        """
        output_record = TransactionOutputRecord.get_byid(
            output_record_id
        )
        output_record.update(**output_infos)
        return output_record

    @classmethod
    def statistics_person_bymonth(cls, person_id):
        """
        统计个人账务通过每月
        """
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
        """
        获取客户余额
        """
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
        """
        获取交易详情
        """
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
        """
        获取入账记录通过入账编号
        """
        return TransactionInputRecord.search(number=number).first()

    @classmethod
    def get_output_record_bynumber(cls, number):
        """
        获取出账记录通过出账编号
        """
        return TransactionOutputRecord.search(number=number).first()

    @classmethod
    def finished_output_record_bynumber(cls, number):
        """
        完成出账单通过出账编号
        """
        output_record = cls.get_output_record_bynumber(number)
        output_record.update(
            status=TransactionStatus.ACCOUNT_FINISH
        )
        return output_record

    @classmethod
    def failure_output_record_bynumber(cls, number):
        """
        完成出账单通过出账编号
        """
        output_record = cls.get_output_record_bynumber(number)
        output_record.update(
            status=TransactionStatus.ACCOUNT_FAIL
        )
        return output_record
