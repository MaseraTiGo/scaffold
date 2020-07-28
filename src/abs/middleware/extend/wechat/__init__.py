# coding=UTF-8

import os
import requests
import hashlib
import xmltodict
import time

from . import utils


class Mini(object):

    def __init__(self, type):
        self.type = type

    @property
    def appid(self):
        return 'wx22a8fc65e8d220af'

    @property
    def appsecret(self):
        return ''

    """小程序登录"""
    def login(self, code):
        params = {
            'appid': self.appid,
            'secret': self.appsecret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        res = requests.get('https://api.weixin.qq.com/sns/jscode2session', params = params).json()
        return res
        # if res.get('openid'):
        #     return res
        # print(res)
        # raise BusinessError('登陆异常')

    """手机号数据解密"""
    def get_info(self, encrypted_data, sessionKey, iv):
        result = utils.decrypt_iv(encrypted_data, sessionKey, iv)
        print(result)
        # if result['watermark']['appid'] != self.appid:
        #     raise BusinessError('微信数据异常')
        # return result


class MiniMch(object):

    def __init__(self, type):
        self.spbill_create_ip = '114.114.114.114'
        self.type = type

    @property
    def appid(self):
        return 'wx22a8fc65e8d220af'

    @property
    def mchid(self):
        return '1517459321'

    @property
    def notify_url(self):
        return ' http://3tzeva.natappfree.cc'

    @property
    def key(self):
        return 'rongmibiquan20181026172354biquan'

    def get_sign(self, param):
        # 计算签名
        url_str = utils.get_urlparam(param)
        stringSignTemp = url_str + '&key=' + self.key
        hl = hashlib.md5()
        hl.update(stringSignTemp.encode(encoding = 'utf-8'))
        return hl.hexdigest().upper()

    def check_sign(self, kwargs):
        check_sign = kwargs.pop('sign')
        sign = self.get_sign(kwargs)
        return bool(check_sign == sign)

    # 统一下单
    def unifiedorder(self, out_trade_no, price, product_id = '',
                     body = '', trade_type = 'NATIVE', openid = ''):
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        notify_url = self.notify_url + '/interface/wechat_top_up_notify'
        param = {
            'appid': self.appid,
            'mch_id': self.mchid,
            'nonce_str': utils.get_nonce_str(),
            'device_info': 'WEB',
            'sign_type': 'MD5',
            'body': body,
            'out_trade_no': out_trade_no,
            'fee_type': 'CNY',
            'total_fee': price,
            'spbill_create_ip': self.spbill_create_ip,
            'notify_url': notify_url,
            'trade_type': trade_type
        }
        if trade_type == 'NATIVE':
            param.update({'product_id': str(product_id)})
        elif trade_type == 'JSAPI':
            param.update({'openid': openid})
        sign = self.get_sign(param)
        param.update({'sign': sign})
        param = {'root': param}
        xml_str = xmltodict.unparse(param)
        resp = requests.post(
            url,
            data = xml_str.encode('utf-8'),
            headers = {'Content-Type': 'text/xml'}
        )
        data = resp.text.encode('ISO-8859-1').decode('utf-8')
        data = xmltodict.parse(data)['xml']
        return data

    # 获取小程序支付参数
    def get_pay_param(self, prepay_id):
        param = {
            'appId': self.appid,
            'timeStamp': int(time.time()),
            'nonceStr': utils.get_nonce_str(),
            'package': 'prepay_id={prepay_id}'.format(prepay_id = prepay_id),
            'signType': 'MD5'
        }
        sign = self.get_sign(param)
        param.update({'paySign': sign})
        return param

    # 获取app支付参数
    def get_app_sign(self, prepay_id):
        param = {
            'appid': self.appid,
            'partnerid': self.mchid,
            'prepayid': prepay_id,
            'package': 'Sign=WXPay',
            'noncestr': utils.get_nonce_str(),
            'timestamp': str(int(time.time())),
        }
        sign = self.get_sign(param)
        param.update({'sign': sign})
        return param


class MiniMchKey(MiniMch):

    def __init__(self, type):
        super(MiniMchKey, self).__init__(type)
        path = os.path.dirname(os.path.realpath(__file__))
        self.cert_pem = os.path.join(path, 'apiclient_cert.pem')
        self.key_pem = os.path.join(path, 'apiclient_key.pem')
        # self.cert_pem = '/var/private/apiclient_cert.pem'
        # self.key_pem = '/var/private/apiclient_key.pem'

    # 加密信息解密
    def req_info_decrypt(self, req_info):
        hl = hashlib.md5()
        hl.update(self.key.encode(encoding = 'utf-8'))
        md5_key = hl.hexdigest().lower()
        return utils.decrypt(req_info, md5_key)

    # 企业付款
    def transfers(self, openid, partner_trade_no, amount, desc):
        url = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers'
        params = {
            'mch_appid': self.appid,
            'mchid': self.mchid,
            'nonce_str': utils.get_nonce_str(),
            'partner_trade_no': partner_trade_no,
            'openid': openid,
            'check_name': 'NO_CHECK',
            'amount': amount,
            'desc': desc,
            'spbill_create_ip': self.spbill_create_ip
        }
        params.update({'sign': self.get_sign(params)})
        params = {'root': params}
        xml = xmltodict.unparse(params)

        res = requests.post(url, data = xml.encode('utf-8'),
                            headers = {'Content-Type': 'text/xml'},
                            cert = (self.cert_pem, self.key_pem))

        msg = res.text
        data = xmltodict.parse(msg)['xml']
        return data
        # if data['return_code'] != 'SUCCESS':
        #     logger.error("提现失败：订单号（{partner_trade_no}），{return_msg}".format(partner_trade_no = partner_trade_no,
        #                                                                     return_msg = data['return_msg']))
        #     return False
        # if data['result_code'] != 'SUCCESS':
        #     logger.error("提现失败：订单号（{partner_trade_no}），{err_code_des}".format(partner_trade_no = partner_trade_no,
        #                                                                     err_code_des = data['err_code_des']))
        #     return False
        # return data

    # 退款
    def refund(self, out_trade_no, out_refund_no, total_fee, refund_fee):
        url = "https://api.mch.weixin.qq.com/secapi/pay/refund"
        notify_url = self.notify_url + '/interface/refund_notify'
        params = {
            "appid": self.appid,
            "mch_id": self.mchid,
            "nonce_str": utils.get_nonce_str(),
            "sign_type": "MD5",
            "out_trade_no": out_trade_no,
            "out_refund_no": out_refund_no,
            "total_fee": total_fee,
            "refund_fee": refund_fee,
            "refund_fee_type": "CNY",
            "notify_url": notify_url
        }
        params.update({'sign': self.get_sign(params)})
        params = {'root': params}
        xml = xmltodict.unparse(params)
        res = requests.post(
            url,
            data = xml.encode('utf-8'),
            headers = {'Content-Type': 'text/xml'},
            cert = (self.cert_pem, self.key_pem)
        )
        msg = res.text
        data = xmltodict.parse(msg)['xml']
        return data
        # if data.get('return_code') != 'SUCCESS':
        #     logger.error('微信退款接口调用失败，退款单号（{out_refund_no}），{return_msg}'\
        #                  .format(out_refund_no = out_refund_no, return_msg = data['return_msg']))
        #     return False
        # if data.get('result_code') != 'SUCCESS':
        #     logger.error('微信退款接口调用失败，退款单号（{out_refund_no}），错误代码：{err_code}，错误描述：{err_code_des}'\
        #                  .format(out_refund_no = out_refund_no, err_code = data['err_code'], err_code_des = data['err_code_des']))
        #     return False
        # return data
