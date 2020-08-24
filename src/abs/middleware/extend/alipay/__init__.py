# coding=UTF-8
import datetime
import json
import os
import base64
import rsa
from urllib.parse import quote_plus
from abs.middleware.config import config_middleware


class AlipayExtend(object):

    def _get_appid(self):
        return config_middleware.get_value("alipay", "appid")
        # return "2019092767881151"

    def _get_notify_url(self):
        return config_middleware.get_value("common", "domain")

    def _get_priv_key(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, "private.pem")
        # file_path = '/var/private/rsa-pkcs1.pem'
        with open(file_path) as f:
            priv_key = f.read()
        return priv_key

    def _get_alipay_public_key(self):
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, "alipay_public.pem")
        # file_path = '/var/private/rsa-pkcs1.pem'
        with open(file_path) as f:
            priv_key = f.read()
        return priv_key

    def get_result_str(self, **params):
        sort_list = sorted([(k, v) for k, v in params.items()])
        unsigned_string = "&".join("{}={}".format(
            k,
            v
        ) for k, v in sort_list)
        signature = self._rsa_sign(unsigned_string)
        quoted_string = "&".join("{}={}".format(
            k,
            quote_plus(v)
        ) for k, v in sort_list)
        result_str = quoted_string + "&sign=" + quote_plus(signature)

        return result_str

    def _rsa_sign(self, encr_data):
        e = rsa.PrivateKey.load_pkcs1(self._get_priv_key())
        sign = rsa.sign(encr_data.encode('utf-8'), e, "SHA-256")
        return base64.b64encode(sign).decode()

    def check_sign(self, params):
        return True

    def _base_params(self):
        return {
            'app_id': self._get_appid(),
            'format': 'JSON',
            'charset': 'utf-8',
            'sign_type': 'RSA2',
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0'
        }

    # 获取app支付信息
    def get_order_info(
            self,
            out_trade_no,
            total_amount,
            notify_path,
            body,
            subject,
            timeout_express = '15d',
            goods_type = '0'
    ):
        method = 'alipay.trade.app.pay'
        params = {
            'method': method,
            'notify_url': self._get_notify_url() + notify_path,
            'biz_content': json.dumps({
                'body': body,
                'subject': subject,
                'out_trade_no': out_trade_no,
                'timeout_express': timeout_express,
                'total_amount': total_amount,
                'product_code': 'QUICK_MSECURITY_PAY',
                'goods_type': goods_type
            })
        }
        params.update(self._base_params())
        return self.get_result_str(**params)


alipay_extend = AlipayExtend()
