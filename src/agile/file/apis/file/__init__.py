# coding=UTF-8
import datetime
from urllib import parse
from infrastructure.core.field.base import CharField, FileField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.base.api import NoAuthorizedApi
from abs.middleware.file import file_middleware
from abs.middleware.oss import OSSAPI

class Upload(NoAuthorizedApi):
    """上传文件"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "文件名称：协议内置参数")
    request.role = RequestField(CharField, desc = "访问服务标识，如：crm")
    request.auth = RequestField(CharField, desc = "访问用户token")
    request.store_type = RequestField(CharField, desc = "上传分类")

    response = with_metaclass(ResponseFieldSet)
    response.file_paths = ResponseField(ListField, desc = '文件路径列表', fmt = CharField(desc = "文件路径列表"))

    @classmethod
    def get_desc(cls):
        return "上传文件"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        store_type = {"school", "major", "goods", "video", \
                      "adsense", "person", "contract", \
                      "agent", "idimg", "other"}
        if request.store_type not in store_type:
            raise BusinessError("此上传分类不存在")
        path_list = []
        for name, f in request._upload_files.items():
            suffix = name.split(".")[-1]
            nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            store_name = "source/{type}/{time}.{suffix}".format(
                type = request.store_type,
                time = nowTime,
                suffix = suffix
            )
            imgurl = OSSAPI().put_object(store_name, f, "orgdeer")
            path_list.append(parse.unquote(imgurl))
        '''
        path_list = []
        for name, f in request._upload_files.items():
            path = file_middleware.save(name, f, request.store_type)
            host_url = ""
            path_list.append(host_url + path)
        '''
        return path_list

    def fill(self, response, path_list):
        response.file_paths = path_list
        return response

