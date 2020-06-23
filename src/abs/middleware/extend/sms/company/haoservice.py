# coding=UTF-8
import requests

from urllib import parse
from .base import SmsBase


class HaoserviceSms(SmsBase):

    url = 'http://apis.haoservice.com/sms/sendv2?'

    def get_label(self):
        return 'haoservice_sms'

    def get_name(self):
        return 'haoservice短信平台'

    def get_sign_name(self):
        return ''

    def get_key(self):
        return ''

    def send(self, phone, template_id, template, sign_name, **kwargs):
        params = {
            'content': '【' + sign_name + '】' + template.content.format(**template.get_params(**kwargs)),
            'key': self.get_key(),
            'mobile': phone,
            'tpl_id': template_id
        }
        url = self.url + parse.urlencode(params)
        result = requests.get(url).json()
        if result.get('error_code') == 0:
            return True
        # logger.error('短信发送失败，原因：{reason}'.format(reason = result.get('reason', '')))
        return False


hao_service = HaoserviceSms()
