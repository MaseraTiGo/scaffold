# coding=UTF-8
import json
import random
import time
from infrastructure.log.base import logger
from . import SmsBase
from abs.middleware.ssocheck import local_sms_middleware


class LocalSms(SmsBase):

    def get_label(self):
        return 'local_sms'

    def get_name(self):
        return '本地短信平台'

    def get_app_key(self):
        return 'e14af238bf184575b3346856732180a8'

    def get_channel_code(self):
        return 'CHL_003'

    def send(self, phone, template_id, sign_name, **kwargs):
        kwargs.update({'mobile': phone})
        params = {
            'appKey': self.get_app_key(),
            'smsType': template_id,
            'channelCode': self.get_channel_code(),
            'requestId': self.generate_sn('SA'),
            'extendData': json.dumps([kwargs])
        }
        result = local_sms_middleware.send_sms(**params)
        if result.get('status') == 'ok':
            return True
        logger.error('短信发送失败，原因：{reason}'.format(reason = result.get('msg', '')))
        return False

    def get_nonce_str(self, length = 32):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        nonce_str = ""
        for i in range(length):
            tmp_len = random.randint(0, len(chars) - 1)
            nonce_str += chars[tmp_len:tmp_len + 1]
        return nonce_str

    def generate_sn(self, prefix):
        """生成订单号"""
        rand_num = str(random.randint(1000, 9999))
        time_mark = str(int(time.time() * 1000))
        sn = prefix + time_mark + rand_num
        return sn


local_sms = LocalSms()
