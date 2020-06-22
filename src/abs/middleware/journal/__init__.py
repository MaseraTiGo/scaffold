# coding=UTF-8

import time

from model.models import Journal, OperationTypes
from infrastructure.utils.common.split_page import Splitor


class JournalMiddleware(object):

    @classmethod
    def register(self, active, active_type, passive, \
                 passive_type, journal_type, record_detail, remark):

        return Journal.create(active_uid = active.id if active else 0, \
                              active_name = active.name if active else "系统", \
                              active_type = active_type if active else OperationTypes.SYSTEM, \
                              passive_uid = passive.id if passive else 0, \
                              passive_name = passive.name if passive else "系统", \
                              passive_type = passive_type if passive else OperationTypes.SYSTEM, \
                              journal_type = journal_type, \
                              record_detail = record_detail, remark = remark)

    @classmethod
    def search(cls, current_page, **search_info):
        """查询日志列表"""
        journal_qs = Journal.search(**search_info)
        journal_qs = journal_qs.order_by("-create_time")
        return Splitor(current_page, journal_qs)
