# coding=UTF-8
import requests
import time
import random
import hashlib
import json

from tuoen.sys.log.base import logger
from tuoen.abs.middleware.config import config_middleware
from .base import SmsBase


class TenxunSms(SmsBase):

    def get_label(self):
        return 'tenxun_sms'

    def get_name(self):
        return '腾讯短信平台'

    def get_sign_name(self):
        return config_middleware.get_value(self.label, 'sign_name')

    def get_appid(self):
        return config_middleware.get_value(self.label, 'appid')

    def get_appkey(self):
        return config_middleware.get_value(self.label, 'appkey')

    def get_sig(self, number, timestamp, phone):
        raw_text = "appkey={appkey}&random={random}&time={time}&mobile={mobile}"\
            .format(appkey=self.get_appkey(), random=number, time=timestamp, mobile=phone)
        return hashlib.sha256(raw_text.encode('utf-8')).hexdigest()

    def send(self, phone, template_id, template, sign_name, **kwargs):
        number = random.randint(10000, 99999)
        url = 'https://yun.tim.qq.com/v5/tlssmssvr/sendsms?sdkappid={appid}&random={number}'\
              .format(appid=self.get_appid(), number=number)
        timestamp = int(time.time())
        sig = self.get_sig(number, timestamp, phone)
        try:
            template_id = int(template_id)
        except:
            return False
        param = {
            'params': list(kwargs.values()),
            'sig': sig,
            'sign': sign_name,
            'tel': {
                'mobile': phone,
                'nationcode': '86'
            },
            'time': timestamp,
            'tpl_id': template_id
        }
        result = requests.post(url, data=json.dumps(param)).json()
        if result.get('result') == 0:
            return True
        logger.error('短信发送失败，原因：{reason}'.format(reason = result.get('errmsg', '')))
        return False


tenxun_sms = TenxunSms()
