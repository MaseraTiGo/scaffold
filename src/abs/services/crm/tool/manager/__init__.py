# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleware.sms import sms_middleware
from abs.services.crm.tool.store.sms import SmsRecord
from abs.services.crm.tool.utils.contact import SceneTypes, SourceTypes


class SmsServer(BaseManager):

    @classmethod
    def send_code(cls, phone, scene, source_type):
        if sms_middleware.send_code(phone, scene, source_type):
            return True
        raise BusinessError('发送失败')

    @classmethod
    def send_msg(cls, phone, scene, unique_no, source_type, **kwargs):
        if sms_middleware.send_msg(phone, scene, unique_no, source_type, **kwargs):
            return True
        raise BusinessError('发送失败或该短信已发送过')

    @classmethod
    def send_register_code(cls, phone):
        cls.send_code(phone, SceneTypes.REGISTER, SourceTypes.CUSTOMER)


class SmsRecordServer(BaseManager):

    @classmethod
    def search(cls, current_page, **search_info):
        record_qs = SmsRecord.search(**search_info).order_by('-create_time')
        return Splitor(current_page, record_qs)
