# coding=UTF-8
import json

from .base import SmsBase
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


class AliSms(SmsBase):

    def get_label(self):
        return 'ali_sms'

    def get_name(self):
        return '阿里短信平台'

    def get_sign_name(self):
        return ''

    def get_key(self):
        return ''

    def get_secret(self):
        return ''

    def send(self, phone, template_id, template, sign_name, **kwargs):
        client = AcsClient(self.get_key(), self.get_secret(), 'default')
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', sign_name)
        request.add_query_param('TemplateCode', template_id)
        request.add_query_param('TemplateParam', kwargs)

        response = client.do_action_with_exception(request)
        result = json.loads(str(response, encoding = 'utf-8'))
        if result.get('Code') == 'OK':
            return True
        # logger.error('短信发送失败，原因：{reason}'.format(reason = result.get('Message', '')))
        return False


ali_sms = AliSms()
