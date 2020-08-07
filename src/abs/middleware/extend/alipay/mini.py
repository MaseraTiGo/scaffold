# coding=UTF-8
import os
import random
import base64
import time
import datetime
import json
import rsa
from urllib.parse import quote_plus
from urllib.request import urlopen


class AlipayMiniExtend(object):

    _url = "https://openapi.alipay.com/gateway.do"
    _head = None

    def get_appid(self):
        return "2014072300007148"

    def get_payee_user_id(self):
        return "2088911513001102"

    def _get_category(self):
        return "RENT_DIGITAL"

    def _get_notify_url(self):
        return 'http://ku4aaz.natappfree.cc'

    def _get_timestamp(self):
        now_time = datetime.datetime.now()
        return now_time.strftime('%Y-%m-%d %H:%M:%S')

    def _get_out_request_no(self):
        """生成订单号"""
        rand_num = str(random.randint(1000, 9999))
        time_mark = str(int(time.time() * 1000))
        sn = 'OUT' + time_mark + rand_num
        return sn

    def _get_priv_key(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, "private.pem")
        # file_path = '/var/private/rsa-pkcs1.pem'
        with open(file_path) as f:
            priv_key = f.read()
        return priv_key

    def get_base_param(self, appid):
        base_param = {
            "app_id": appid,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": self._get_timestamp(),
            "version": "1.0"
        }
        return base_param

    def _ordered_data(self, data):
        complex_keys = [k for k, v in data.items() if isinstance(v, dict)]
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))
        return sorted([(k, v) for k, v in data.items()])

    def _get_splicing_str(self, **param):
        ordered_items = self._ordered_data(param)
        unsigned_string = "&".join("{}={}".format(
            k,
            v
        ) for k, v in ordered_items)
        signature = self._rsa_sign(unsigned_string)
        quoted_string = "&".join("{}={}".format(
            k,
            quote_plus(v)
        ) for k, v in ordered_items)
        signed_string = quoted_string + "&sign=" + quote_plus(signature)
        return signed_string

    def _rsa_sign(self, encr_data):
        e = rsa.PrivateKey.load_pkcs1(self._get_priv_key())  # load 公钥，由于之前生成的私钥缺少'RSA'字段，故无法 load
        sign = rsa.sign(encr_data.encode('utf-8'), e, "SHA-256")  # 使用私钥进行'sha256'签名
        return base64.b64encode(sign).decode()

    def _pack_capital(self, method, appid, **param):
        """资金冻结打包方法"""
        base_param = self.get_base_param(appid)
        base_param.update({
            "method": method,
            "biz_content": json.dumps(param, separators=(',', ':'))
        })
        notify_url = self._get_notify_url() + '/interface/alipay_freeze_notify'
        if notify_url:
            base_param.update({
                "notify_url": notify_url
            })
        result_data = self._get_splicing_str(**base_param)
        return result_data

    def _pack(self, method, appid, **param):
        base_param = self.get_base_param(appid)
        base_param.update({
            "method": method
        })
        re_data = self._get_splicing_str(**dict(base_param, **param))
        return re_data

    def _request_api(self, pack_type, method, appid, **param):
        result_content = None
        if param is not None:
            if pack_type == "no_biz":
                sign_data = self._pack(method, appid, **param)
            else:
                sign_data = self._pack_capital(method, appid, **param)
            url = self._url + "?" + sign_data
            result_content = json.loads(self.send(url))
        return result_content

    def send(self, url):
        result = urlopen(url, timeout=15).read().decode("utf-8")
        return result

    """资金冻结查询"""
    def alipay_freeze_query(self, **dic_param):
        method = "alipay.fund.auth.operation.detail.query"
        params = {
            "auth_no": dic_param["auth_no"],
            "operation_id": dic_param["operation_id"]
        }
        result = self._request_api('have_biz', method, self.get_appid(), **params)
        return result

    """资金冻结"""
    def alipay_freeze(self, **dic_param):
        method = "alipay.fund.auth.order.app.freeze"
        params = {
            "out_order_no": "{order_sn}{time_mark}".format(
                order_sn=dic_param["order_no"],
                time_mark=str(int(time.time() * 1000))
            ),
            "out_request_no": self._get_out_request_no(),
            "order_title": "授权冻结",
            "amount": dic_param["amount"] / 100,
            "product_code": "PRE_AUTH_ONLINE",
            "payee_user_id": self.get_payee_user_id(),
            "extra_param": {
                "category": self._get_category()
            }
        }
        result_str = self._pack_capital(method, self.get_appid(), **params)
        return result_str

    """资金授权解冻"""
    def alipay_unfreeze(self, **dic_param):
        method = "alipay.fund.auth.order.unfreeze"
        params = {
            "auth_no": dic_param["auth_no"],
            "out_request_no": self._get_out_request_no(),
            "remark": "{unfreeze_time}解冻{money}".format(
                unfreeze_time=self._get_timestamp(),
                money=dic_param["amount"] / 100
            ),
            "amount": dic_param["amount"] / 100
        }
        if dic_param["deposit_type"] == "credit":  # 冻结类型，押金or信用分
            params.update({
                "extra_param": {
                    "unfreezeBizInfo": "{\"bizComplete\":\"true\"}"
                }
            })
        result = self._request_api('have_biz', method, self.get_appid(), **params)
        return result

    """资金授权转支付"""
    def alipay_freeze_trade(self, **dic_param):
        method = "alipay.trade.pay"
        params = {
            "out_trade_no": self._get_out_request_no(),
            "auth_no": dic_param["auth_no"],
            "product_code": "PRE_AUTH_ONLINE",
            "subject": "预授权转支付",
            "buyer_id": dic_param["buyer_id"],
            "seller_id": dic_param["seller_id"],
            "total_amount": dic_param["total_amount"] / 100,
            "auth_confirm_mode": "COMPLETE"
        }
        result = self._request_api('have_biz', method, self.get_appid(), **params)
        return result

    """获取支付宝小程序user_id"""
    def get_user_id(self, code):
        method = "alipay.system.oauth.token"
        params = {
            "grant_type": "authorization_code",
            "code": code
        }
        result = self._request_api("no_biz", method, self.get_appid(), **params)
        return result

    """生成二维码"""
    def get_chance_qrcode(self, **dic_param):
        method = "alipay.open.app.qrcode.create"
        items = self._ordered_data(dic_param["data"])
        query_param = "&".join("{}={}".format(k, v) for k, v in items)
        params = {
            "url_param": dic_param["url_param"],
            "query_param": query_param,
            "describe": dic_param["describe"]
        }
        result = self._request_api(
            "have_biz",
            method,
            self.get_appid(),
            **params
        )
        return result


alipay_mini_extend = AlipayMiniExtend()
