# coding=UTF-8

from infrastructure.core.service.base import BaseAPIService
from abs.middleware.rule import rule_register, \
            permise_rules

# from agile.apis import test


class FileService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "文件服务"

    @classmethod
    def get_desc(self):
        return "提供文件上传服务"

    @classmethod
    def get_flag(cls):
        return "file"


# file_service = FileService()
# from agile.apis.file import Upload
# file_service.add(Upload)
