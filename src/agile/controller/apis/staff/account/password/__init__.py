# coding=UTF-8

'''
Created on 2020年7月5日

@author: Roy
'''

from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.field.base import CharField, IntField
from infrastructure.core.exception.business_error import BusinessError

from agile.controller.manager.api import StaffAuthorizedApi
from abs.services.controller.account.manager import StaffAccountServer


class Modify(StaffAuthorizedApi):
    """
    修改密码（用于员工自身修改密码使用）
    """
    request = with_metaclass(RequestFieldSet)
    request.old_password = RequestField(CharField, desc="老密码")
    request.new_password = RequestField(CharField, desc="新密码")
    request.repeat_password = RequestField(CharField, desc="重复新密码")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工修改密码接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        staff = self.auth_user
        if request.new_password != request.repeat_password:
            raise BusinessError("两次输入密码不一致")
        StaffAccountServer.modify_password(
            staff.id,
            old_password=request.old_password,
            new_password=request.new_password
        )

    def fill(self, response, token):
        return response


class Reset(StaffAuthorizedApi):
    """
    重置密码（用于针对员工重置使用）
    """
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc="员工id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        StaffAccountServer.reset_password(
            request.staff_id,
        )

    def fill(self, response, token):
        return response
