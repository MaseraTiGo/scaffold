# coding=UTF-8
import requests
import time
import random
import hashlib
import json

from tuoen.sys.log.base import logger
from tuoen.abs.middleware.config import config_middleware
from .base import SmsBase


class WangyiSms(SmsBase):

    def get_label(self):
        return 'wangyi_sms'

    def get_name(self):
        return '网易短信平台'

    def get_sign_name(self):
        return config_middleware.get_value(self.label, 'sign_name')

    def get_appkey(self):
        return config_middleware.get_value(self.label, 'appkey')

    def get_appsecret(self):
        return config_middleware.get_value(self.label, 'appsecret')

    def _get_current_time(self):
        return int(time.time())

    def _get_random_number(self):
        return random.randint(1000000000, 9999999999)

    def _get_headers(self):
        str_time = str(self._get_current_time())
        str_noce = str(self._get_random_number())
        appkey = self.get_appkey()
        appsecret = self.get_appsecret()
        content_type = 'application/x-www-form-urlencoded;charset=utf-8'
        str_header = "{appsecret}{noce}{curtime}".format(appsecret=appsecret, \
                                                         noce=str_noce, \
                                                         curtime=str_time).encode(encoding='utf_8')
        checksum = hashlib.sha1(str_header).hexdigest()
        return {'content-type': content_type, "appKey": appkey, \
                "nonce": str_noce, "curTime": str_time, "CheckSum": checksum}

    def send(self, phone, template_id, template, sign_name, **kwargs):
        headers = self._get_headers()
        url = 'https://api.netease.im/sms/sendtemplate.action'
        param = {
            'mobiles': json.dumps([phone]),
            'templateid': int(template_id),
            'params': json.dumps(list(kwargs.values()))
        }
        result = requests.post(url, headers=headers, data=param).json()
        if result.get('code') == 200:
            return True
        logger.error('短信发送失败，原因：{reason}'.format(reason = result.get('msg', '')))
        return False


wangyi_sms = WangyiSms()
