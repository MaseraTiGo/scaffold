# coding=UTF-8
import requests
import time
import hmac
import hashlib
import json
from urllib import parse
from .base import SmsBase


class BaiduSms(SmsBase):

    def get_label(self):
        return 'baidu_sms'

    def get_name(self):
        return '百度短信平台'

    def get_sign_name(self):
        return ''

    def get_access_key_id(self):
        return ''

    def get_access_key_secret(self):
        return ''

    def hmac_sha256_hex(self, key, auth_str):
        signature = hmac.new(bytes(key, encoding='utf-8'), bytes(auth_str, encoding='utf-8'), digestmod=hashlib.sha256).digest()
        return signature.hex().lower()

    def sha256_hex(self, param_str):
        hash = hashlib.sha256()
        hash.update(param_str.encode('utf-8'))
        return hash.hexdigest()

    def send(self, phone, template_id, template, sign_name, **kwargs):
        url = 'sms.bj.baidubce.com'
        query_str = '/bce/v2/message'

        now_gmtime = time.gmtime()
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", now_gmtime)
        timestamp_day = time.strftime("%Y-%m-%d", now_gmtime)
        access_key_id = self.get_access_key_id()
        access_key_secret = self.get_access_key_secret()
        auth_str = 'bce-auth-v1/{accessKeyId}/{timestamp}/1800/'.format(accessKeyId=access_key_id, timestamp=timestamp)
        signing_key = self.hmac_sha256_hex(access_key_secret, auth_str)

        request_param = {
            "invokeId": sign_name,
            "phoneNumber": phone,
            "templateCode": template_id,
            "contentVar": kwargs
        }
        request_sha256 = self.sha256_hex(json.dumps(request_param))
        headers = {
            'Content-type': 'application/json',
            'x-bce-date': timestamp_day,
            'Host': url,
            'x-bce-content-sha256': request_sha256
        }
        canonical_headers = [i.lower()+':'+parse.urlencode(j) for i, j in headers.items()]
        canonical_headers.sort()
        canonical_headers_str = '\n'.join(canonical_headers)
        canonical_request = 'POST' + "\n" + query_str + "\n" + canonical_headers_str

        signature = self.hmac_sha256_hex(signing_key, canonical_request)
        authorization = auth_str + '/' + signature
        headers.update({'Authorization': authorization})
        result = requests.post(url+query_str, data=json.dumps(request_param), headers=headers).json()
        if result.get('code') == '1000':
            return True
        # logger.error('短信发送失败，原因：{reason}'.format(reason = result.get('message', '')))
        return False


baidu_sms = BaiduSms()
