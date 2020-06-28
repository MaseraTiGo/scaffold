# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService


class FileService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "文件服务"

    @classmethod
    def get_desc(self):
        return "文件传输服务"

    @classmethod
    def get_flag(cls):
        return "file"


file_service = FileService()
from agile.file.apis.file import Upload
file_service.add(Upload)

