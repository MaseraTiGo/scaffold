# coding=UTF-8
import requests
import time
import json
import hashlib
import datetime
import base64
import xmltodict
from Crypto.Cipher import AES
from collections import OrderedDict

# from tuoen.settings import FILE_CONF
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.utils.common.signature import unique_parms, generate_signature
from tuoen.abs.middleware.config import config_middleware
from tuoen.abs.middleware.transport.base import HttpTransport

from model.store.model_logistics import Logistics


class ShunfengTransport(HttpTransport):

    def __init__(self):
        # self._url = "http://bspoisp.sit.sf-express.com:11080/bsp-oisp/sfexpressService"  # 测试
        self._url = "http://bsp-oisp.sf-express.com/bsp-oisp/sfexpressService"  # 正式

    def _get_head(self):
        return config_middleware.get_value("shunfeng", "client_code")

    def _get_checkword(self):
        return config_middleware.get_value("shunfeng", "check_word")

    def get_verifyCode(self, xml):
        connect_str = "{xml}{key}".format(xml = xml, key = self._get_checkword())
        connect_str = hashlib.md5(connect_str.encode("utf-8")).digest()
        connect_str = base64.b64encode(connect_str).decode("utf-8")
        return connect_str

    def query(self, logistics):
        """物流查询"""
        param = OrderedDict()
        param["Request"] = OrderedDict()
        param["Request"]["@service"] = "RouteService"
        param["Request"]["@lang"] = "zh-CN"
        param["Request"]["Head"] = self._get_head()
        param["Request"]["Body"] = OrderedDict()
        param["Request"]["Body"]["RouteRequest"] = OrderedDict()
        param["Request"]["Body"]["RouteRequest"]["@tracking_type"] = "1"
        param["Request"]["Body"]["RouteRequest"]["@method_type"] = "1"
        param["Request"]["Body"]["RouteRequest"]["@tracking_number"] = "444070546609"
        xml = xmltodict.unparse(param)

        connect_str = self.get_verifyCode(xml)
        data = {"xml":xml, "verifyCode":connect_str}
        result = self._request_api(**data)
        result_text = self._get_response_data(result)
        print("=====>>>>>>>333333", result_text)

    def _request_api(self, **data):
        result = requests.post(self._url, data = data)
        return result

    def _get_response_data(self, result):
        result_text = result.text
        result_text = xmltodict.parse(result_text)
        if result_text["Response"]["Head"] == "OK":
            return result_text
        return None

shunfeng_transport = ShunfengTransport()
