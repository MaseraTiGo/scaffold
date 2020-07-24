# coding=UTF-8

from . import TemplateBase


class VerifyCodeSMS(TemplateBase):

    def get_label(self):
        return 'verify_code'

    def get_name(self):
        return '验证码'

    def get_params(self, code):
        return {'code': code}

    def get_content(self):
        return '您的动态验证码为{code}，请在页面输入完成验证。如非本人操作请忽略。'

    def verify_unique_no(self, *args, **kwargs):
        return True


verify_code_sms = VerifyCodeSMS()
