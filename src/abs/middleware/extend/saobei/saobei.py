# coding=UTF-8

import time
import json
import hashlib
import datetime
import requests


class SaobeiExtend(object):


    def __init__(self):
        self._head = {"Content-Type": "application/json"}

    def get_notify_url(self):
        return  # "http://gk7s82.natappfree.cc"  # 回调地址

    def get_merchant_no(self):  # 商户号
        return  # "852107375000003"

    def get_terminal_id(self):
        return  # "11718626"  # 终端号

    def get_access_token(self):
        return  # "ecd84189573343cca3035b8c4fafb556"  # access_token

    def get_fromal_url(self):
        return  # "http://pay.lcsw.cn/lcsw"  # 请求连接

    def _md5(self, md5_str):
        return hashlib.md5(md5_str.encode("utf-8")).hexdigest()

    def get_sign(self, sign_str):
        md5_str = "{sign_str}&access_token={access_token}".format(sign_str = sign_str, access_token = self.get_access_token())
        sign = self._md5(md5_str)
        return sign

    def _pack(self, **param):
        sign_str = ""
        if len(param) > 0:
            param_key = sorted(param.keys(), reverse = False)
            for key in param_key:
                if sign_str == "":
                    sign_str = "{sign_str}{key}={value}".format(sign_str = sign_str, key = key, value = param[key])
                else:
                    sign_str = "{sign_str}&{key}={value}".format(sign_str = sign_str, key = key, value = param[key])
        sign = self.get_sign(sign_str)
        param.update({"key_sign":sign})
        return param

    def _request_api(self, url, **param):
        param = self._pack(**param)
        url = "{baseurl}{url}".format(baseurl = self.get_fromal_url(), url = url)
        result = self.send(url, self._head, **param)
        result_data = json.loads(result.decode("utf-8"))
        return result_data

    def send(self, url, headers, **body):
       result = requests.post(url, data = json.dumps(body), headers = headers)
       result_str = result.content
       return result_str

    def get_qrpay_url(self, dic_param):
        """获取聚合码支付二维码url"""
        notify_url = self.get_notify_url() + '/interface/saobei_notify'
        url = "/pay/110/qrpay"
        test_data = {"pay_ver":"130", "pay_type":"000", "service_id":"016", \
                     "merchant_no":self.get_merchant_no(), "terminal_id":self.get_terminal_id(), \
                     "terminal_trace": dic_param["terminal_trace"], "terminal_time": dic_param["terminal_time"], \
                     "total_fee": dic_param["total_fee"], "order_body": dic_param["body"], "notify_url":notify_url}
        result = self._request_api(url, **test_data)
        return result

    def query(self, dic_param):
        """支付结果查询接口"""
        url = "/pay/110/query"
        test_data = {"pay_ver":"100", "pay_type":"000", "service_id":"020", \
                     "merchant_no":self.get_merchant_no(), "terminal_id":self.get_terminal_id(), \
                     "terminal_trace": str(int(time.time() * 100000)), "terminal_time": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                     "pay_trace": dic_param["pay_trace"], "pay_time": dic_param["pay_time"]}
        result = self._request_api(url, **test_data)
        return result

    def refund(self, dic_param):
        """退款申请接口"""
        url = "/pay/110/refund"
        test_data = {"pay_ver":"100", "pay_type":"000", "service_id":"030", \
                     "merchant_no":self.get_merchant_no(), "terminal_id":self.get_terminal_id(), \
                     "terminal_trace": dic_param["terminal_trace"], "terminal_time": dic_param["terminal_time"], \
                     "refund_fee":dic_param["refund_fee"], "out_trade_no": dic_param["out_trade_no"]}
        result = self._request_api(url, **test_data)
        return result

    def queryrefund(self, dic_param):
        """退款订单查询接口"""
        url = "/pay/110/queryrefund"
        test_data = {"pay_ver":"100", "pay_type":"000", "service_id":"031", \
                     "merchant_no":self.get_merchant_no(), "terminal_id":self.get_terminal_id(), \
                     "terminal_trace":str(int(time.time() * 100000)), "terminal_time":datetime.datetime.now().strftime("%Y%m%d%H%M%S"), \
                     "pay_trace": dic_param["pay_trace"], "pay_time": dic_param["pay_time"]}
        result = self._request_api(url, **test_data)
        return result


saobei_extend = SaobeiExtend()
