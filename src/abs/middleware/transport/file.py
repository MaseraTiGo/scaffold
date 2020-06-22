# coding=UTF-8

import time
import json
import requests
from src.settings import FILE_CONF
from infrastructure.utils.common.dictwrapper import DictWrapper
from infrastructure.utils.common.signature import unique_parms, generate_signature
from abs.middleware.transport.base import HttpTransport


class FileTransport(HttpTransport):

    def __init__(self, files, headers = None):
        self._files = files

    def _get_flag(self):
        return "file"

    def _get_api(self):
        return "file.upload"

    def _get_file_url(self):
        return "http://{}:{}/interface/"\
            .format(FILE_CONF['host'], FILE_CONF['port'])

    def _get_current_time(self):
        return int(time.time())

    def _generate_signature(self, parms):
        unique_string, length = unique_parms(parms)
        return generate_signature(unique_string, length)

    def _combination_parms(self, **kwargs):
        parms = {
            "timestamp": self._get_current_time()
        }
        parms.update(kwargs)
        sign = self._generate_signature(parms)
        parms.update({"sign": sign})
        return parms

    def _get_response_data(self, result):
        result = DictWrapper(result)
        status = result.status
        if status != "ok":
            return None
        return result.result

    @classmethod
    def is_fileserver(cls, request_ip):
        if request_ip in ['localhost', '127.0.0.1']:
            return True
        return FILE_CONF['host'] == request_ip

    @classmethod
    def get_server_host(cls):
        host_url = "http://{}".format(FILE_CONF['host'])
        if FILE_CONF['port'] != "80":
            host_url = "{}:{}".format(host_url, FILE_CONF['port'])
        return host_url

    def send(self, request):
        flag = self._get_flag()
        api = self._get_api()
        url = self._get_file_url()

        access_parms = self._combination_parms(flag = flag, api = api, **request)
        result = requests.post(url, data = access_parms, files = self._files)
        return self._get_response_data(result.json())
