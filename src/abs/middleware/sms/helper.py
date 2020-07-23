# coding=UTF-8
import random
import json
import string

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.cache.redis import redis

from abs.services.crm.tool.store.sms import SmsRecord
from abs.services.crm.tool.utils.contact import StatusTypes


class CodeHelper(object):

    _verify_key = '{phone}_{scene}'

    def __init__(self, phone, scene, source_type):
        self.phone = phone
        self.scene = scene
        self.source_type = source_type
        self._key = self._verify_key.format(
            phone=self.phone,
            scene=self.scene
        )

    def generate_code(self):
        code = str(random.randint(100000, 999999))
        return code

    def get_verify_code(self):
        try:
            return redis.get(self._key)
        except Exception as e:
            return None

    def set_verify_code(self, verify_code):
        expire_time = 900
        cur_expire_time = redis.ttl(self._key)
        if cur_expire_time and expire_time - cur_expire_time < 60:
            raise BusinessError('请不要在一分钟内重复获取验证码')
        return redis.set(self._key, verify_code, ex = expire_time)

    def check(self, code):
        verify_code = self.get_verify_code()
        if not verify_code or verify_code.lower() != code.lower():
            return False
        redis.delete(self._key)
        return True

    def send(self, company, template, template_id, sign_name):
        code = self.generate_code()
        self.set_verify_code(code)
        kwargs = {'code': code}
        result = company.send(self.phone, template_id, sign_name, **kwargs)
        status = StatusTypes.FAIL
        flag = False
        if result:
            status = StatusTypes.SUCCESS
            flag = True
        SmsRecord.create(
            phone=self.phone,
            template_id=template_id,
            template_label=template.label,
            label=company.label,
            param=json.dumps(template.get_params(code)),
            content='【' + sign_name + '】' + template.content,
            unique_no='',
            scene=self.scene,
            status=status,
            source_type=self.source_type
        )
        return flag


class MessageHelper(object):

    def __init__(self, phone, scene, unique_no, source_type):
        self.phone = phone
        self.unique_no = unique_no
        self.source_type = source_type
        self.scene = scene

    def send(self, company, template, template_id, sign_name, **kwargs):
        if not template.verify_unique_no(self.phone, self.unique_no):
            return False
        result = company.send(self.phone, template_id, template, sign_name, **kwargs)
        status = StatusTypes.FAIL
        flag = False
        if result:
            status = StatusTypes.SUCCESS
            flag = True
        SmsRecord.create(
            phone=self.phone,
            template_id=template_id,
            template_label=template.label,
            label=company.label,
            param=json.dumps(template.get_params(**kwargs)),
            content='【' + sign_name + '】' + template.content,
            unique_no=self.unique_no,
            scene=self.scene,
            status=status,
            source_type=self.source_type
        )
        return flag
