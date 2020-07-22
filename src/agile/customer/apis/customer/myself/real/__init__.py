# coding=UTF-8

from infrastructure.core.field.base import CharField, IntField, \
        DictField, ListField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.customer.manager.api import CustomerAuthorizedApi
from src.abs.middleware.extend.yunaccount import yunaccount_extend
from abs.middleground.business.person.manager import PersonServer


class Authenticate(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.certification_info = RequestField(DictField, desc="认证信息", conf={
        'name': CharField(desc="姓名"),
        'identification': CharField(desc="身份证"),
        'id_front': CharField(desc="身份证正面"),
        'id_back': CharField(desc="身份证反面"),
        'id_in_hand': CharField(desc='手持身份证')
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "实名认证"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        flag, result = yunaccount_extend.verify_identity(
            request.certification_info['name'],
            request.certification_info['identification']
        )
        if not flag:
            raise BusinessError('姓名与身份证号不匹配')
        customer = self.auth_user
        PersonServer.add_certification(
            customer.person_id,
            **request.certification_info
        )

    def fill(self, response):
        return response


class Get(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.certification_info = ResponseField(DictField, desc="认证信息", conf={
        'name': CharField(desc="姓名"),
        'identification': CharField(desc="身份证"),
        'id_front': CharField(desc="身份证正面"),
        'id_back': CharField(desc="身份证反面"),
        'id_in_hand': CharField(desc='手持身份证')
    })

    @classmethod
    def get_desc(cls):
        return "实名认证"

    @classmethod
    def get_author(cls):
        return "xyc"

    def execute(self, request):
        customer = self.auth_user
        certification = PersonServer.get_person_certification(
            customer.person_id
        )
        return certification

    def fill(self, response, certification):
        response.certification_info = {
            'name': certification.name,
            'identification': certification.identification,
            'id_front': certification.id_front,
            'id_back': certification.id_back,
            'id_in_hand': certification.id_in_hand
        }
        return response
