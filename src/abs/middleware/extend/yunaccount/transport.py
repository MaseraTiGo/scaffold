# coding=UTF-8

import time
import json
import pyDes
import base64
import hmac
import random
import hashlib
import requests


class YunaccountTransport(object):

    def __init__(self):
        self._url = 'https://api-jiesuan.yunzhanghu.com'

    def get_dealer_id(self):
        return '22730335'  # 商户平台ID

    def get_broker_id(self):
        return '27532644'  # 综合服务主体

    def get_des3key(self):
        return "PlqlJ82Ennh02IpaudE3y8H0"  # 3DES Key

    def get_key(self):
        return "BrD14dw7JV97NfNeG72tFqv509CDtudZ"  # App Key

    def get_notify_url(self):
        return "http://yxjcch.natappfree.cc"  # 回调地址

    def get_timestamp(self):
        return int(time.time())

    def get_mess(self):
        rand_num = str(random.randint(1000, 9999))
        time_mark = str(int(time.time()))
        mess = time_mark + rand_num
        return mess

    def get_request_id(self):
        rand_num = str(random.randint(1000, 9999))
        time_mark = str(int(time.time()))
        request_id = "YUN" + time_mark + rand_num
        return request_id

    def get_encryption(self, param):
        param.update({"dealer_id": self.get_dealer_id(), "broker_id": self.get_broker_id()})
        des3key = self.get_des3key()
        iv = des3key[0:8]
        data = json.dumps(param)
        k = pyDes.triple_des(des3key, pyDes.CBC, iv, pad = None, padmode = pyDes.PAD_PKCS5)
        d = k.encrypt(data)
        result_encry = base64.b64encode(d)
        return result_encry

    def get_decrypt(self, encry_data):
        result_encry = base64.b64decode(encry_data)
        des3key = self.get_des3key()
        iv = des3key[0:8]
        k = pyDes.triple_des(
            des3key,
            pyDes.CBC,
            iv,
            pad = None,
            padmode = pyDes.PAD_PKCS5
        )
        result_mampping = json.loads(k.decrypt(result_encry).decode())
        return result_mampping

    def get_sign(self, encry_data, mess, timestamp):
        key = self.get_key()
        sign_str = "data={data}&mess={mess}&timestamp={timestamp}&key={key}".format(
            data = encry_data,
            mess = mess,
            timestamp = timestamp,
            key = key
        )
        sign_str = sign_str.encode(encoding = 'utf_8')
        appkey = key.encode(encoding = 'utf_8')
        signature = hmac.new(
            appkey,
            sign_str,
            digestmod = hashlib.sha256
        ).hexdigest()
        return signature

    def _pack(self, str_encry):
        post_data = {}
        mess = self.get_mess()
        timestamp = self.get_timestamp()
        sign = self.get_sign(str_encry, mess, timestamp)
        post_data.update({
            "data": str_encry,
            "mess": mess,
            "timestamp": timestamp,
            "sign": sign,
            "sign_type": "sha256"
        })
        return post_data

    def get_headers(self):
        return {
            "dealer-id": self.get_dealer_id(),
            "request-id": self.get_request_id()
        }

    def _request_api(self, url, **param):
        str_encry = self.get_encryption(param).decode()
        post_data = self._pack(str_encry)
        url = "{baseurl}{url}".format(baseurl = self._url, url = url)
        result = requests.post(
            url,
            data = post_data,
            headers = self.get_headers()
        )
        result_str = result.content
        result_data = json.loads(result_str.decode("utf-8"))
        return result_data

    def transfers(self, order_sn, real_name, card_no, phone_no, id_card, money):
        """打款"""
        url = "/api/payment/v1/order-realtime"
        notify_path = '/interface/yunaccount_transfer_notify'
        param = {
            "order_id": order_sn,
            "real_name": real_name,
            "card_no": card_no,
            "phone_no": phone_no,
            "id_card": id_card,
            "pay": money,
            "notify_url": self.get_notify_url() + notify_path,
        }
        result = self._request_api(url, **param)
        return result

    def transfers_for_alipay(self, dic_param):
        """支付宝打款"""
        url = "/api/payment/v1/order-alipay"
        param = {
            "order_id": dic_param["order_id"],
            "real_name": dic_param["real_name"],
            "id_card": dic_param["id_card"],
            "card_no": dic_param["card_no"],
            "pay": dic_param["pay"],
            "check_name": "Check",
            "notify_url": self.get_notify_url(),
        }
        result = self._request_api(url, **param)
        return result

    def verify_identity(self, name, identity):
        """姓名身份证号验证"""
        url = "/authentication/verify-id"
        param = {
            'id_card': identity,
            'real_name': name
        }
        result = self._request_api(url, **param)
        return result

    def verify_bankcard_three_factor(self, name, identity, card_no):
        """银行三要素"""
        url = "/authentication/verify-bankcard-three-factor"
        param = {
            'card_no': card_no,
            'id_card': identity,
            'real_name': name
        }
        result = self._request_api(url, **param)
        return result

    def verify_bankcard_four_factor(self, name, identity, card_no, phone):
        """银行卡四要素"""
        url = '/authentication/verify-bankcard-four-factor'
        param = {
            'card_no': card_no,
            'id_card': identity,
            'real_name': name,
            'mobile': phone
        }
        result = self._request_api(url, **param)
        return result


yunaccount_transport = YunaccountTransport()
