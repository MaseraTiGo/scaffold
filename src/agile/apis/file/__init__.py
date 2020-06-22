# coding=UTF-8

from infrastructure.core.field.base import CharField, FileField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet

from agile.apis.server import MiniAuthorizedApi
from abs.middleware.file import file_middleware
from abs.middleware.transport.file import FileTransport


class Upload(MiniAuthorizedApi):
    """上传文件"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "文件名称")
    request._ip = RequestField(CharField, desc = "上传分类")
    request.store_type = RequestField(CharField, desc = "上传分类")

    response = with_metaclass(ResponseFieldSet)
    response.file_paths = ResponseField(ListField, desc = '文件路径列表', fmt = CharField(desc = "文件路径列表"))

    count = False

    @classmethod
    def get_desc(cls):
        return "上传文件"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        path_list = []
        if not FileTransport.is_fileserver(request._ip):
            ft = FileTransport(request._upload_files)
            result = ft.run(store_type = request.store_type)
            path_list = result.file_paths
        else:
            for name, f in request._upload_files.items():
                path = file_middleware.save(name, f, request.store_type)
                host_url = FileTransport.get_server_host()
                path_list.append(host_url + path)
        print(path_list)
        return path_list

    def fill(self, response, path_list):
        response.file_paths = path_list
        return response

