# coding=UTF-8
import json
from infrastructure.core.field.base import CharField, DictField, \
        IntField, ListField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from infrastructure.core.exception.business_error import BusinessError
from agile.customer.manager.api import CustomerAuthorizedApi
from abs.services.customer.personal.utils.constant import FeedType
from abs.services.customer.personal.manager import FeedbackServer


class Add(CustomerAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.feedback_info = RequestField(
        DictField,
        desc = "意见反馈详情",
        conf = {
                'type': CharField(
                    desc = "意见反馈类型",
                    choices = FeedType.CHOICES
                ),
                'describe': CharField(desc = "意见反馈类容"),
                'img_url':ListField(
                    desc = '反馈图片',
                    fmt = CharField(desc = "图片地址"),
                    is_required = False
                ),
        }
    )

    response = with_metaclass(ResponseFieldSet)


    @classmethod
    def get_desc(cls):
        return "意见反馈添加接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        customer = self.auth_user
        img_url = request.feedback_info.pop("img_url", None)
        if img_url:
            if len(img_url) > 3:
                raise BusinessError("最多上传三张图片")
            request.feedback_info.update({
                "img_url":json.dumps(img_url)
            })
        request.feedback_info.update({
            "customer":customer
        })
        FeedbackServer.create(**request.feedback_info)

    def fill(self, response):
        return response