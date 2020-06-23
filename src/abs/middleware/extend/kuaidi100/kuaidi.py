# coding=UTF-8

import json
import hashlib
import requests

# from tuoen.settings import FILE_CONF
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.abs.middleware.config import config_middleware
from tuoen.abs.middleware.transport.base import HttpTransport


class Kuaidi100Extend(object):


    def __init__(self):
        self._schema = "json"
        self._Head = None
        self._company = {"顺丰":"shunfeng", "EMS":"ems", "ems":"ems", "申通":"shentong", "圆通":"yuantong", \
                         "中通":"zhongtong", "汇通":"huitongkuaidi", "韵达":"yunda", "宅急送":"zhaijisong", \
                         "天天":"tiantian", "德邦":"debangwuliu", "能达":"ganzhongnengda", "优速":"youshuwuliu", \
                         "京东":"jd"}

    def get_key(self):
        return  # "kdzcSxGU9830"  # Key

    def get_customer(self):
        return  # "801C05EFA7846366EAA1F95389F309DA"  # 账户密钥

    def get_fromal_url(self):
        return  # "https://poll.kuaidi100.com/poll"  # 请求连接

    def get_notify_url(self):
        return  # "http://crm_test.dsggy.cn"  # 回调地址

    def _get_company_code(self, company_name):
        code = "shunfeng"
        for key, value in self._company.items():
            if key in company_name:
                code = value
                break
        return code

    def _request_api(self, url, **param):
        result = requests.post(url, data = param, headers = self._Head)
        result_str = result.content
        result_data = json.loads(result_str.decode("utf-8"))
        return result_data

    def subscribe(self, dic_param):
        """物流订阅"""
        url = self.get_fromal_url()
        data = {
              "schema":self._schema,
              "param":json.dumps({
                       "company":dic_param["company"],  # 物流公司
                       "number":dic_param["number"],  # 快递单号
                       "to":dic_param["to"],  # 到件的省市区
                       "key": self.get_key(),
                       "parameters":{
                                     "callbackurl":self.get_notify_url()
                                     }
                       })
              }
        result = self._request_api(url, **data)
        return result

    def query(self, dic_param):
        """物流查询"""
        url = "{baseurl}/query.do".format(baseurl = self.get_fromal_url())
        param = json.dumps({
            'com': self._get_company_code(dic_param["com"]),  # 物流公司
            'num': dic_param["num"],  # 物流单号
            "to": dic_param["to"],  # 到件的省市区
        })
        customer = self.get_customer()
        sign_str = '{param}{key}{customer}'.format(param = param, key = self.get_key(), customer = customer)
        sign = hashlib.md5(sign_str.encode(encoding = 'UTF-8')).hexdigest().upper()
        data = {
            'customer': customer,
            'sign': sign,
            'param': param
        }
        result = self._request_api(url, **data)
        return result


kuaidi100_extend = Kuaidi100Extend()
