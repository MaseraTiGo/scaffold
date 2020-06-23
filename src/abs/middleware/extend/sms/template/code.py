# coding=UTF-8

from tuoen.abs.middleware.extend.sms.template import TemplateBase


class VerifyCodeSMS(TemplateBase):

    def get_label(self):
        return 'verify_code'

    def get_name(self):
        return '验证码'

    def get_params(self, code):
        return {'code': code}

    def verify_unique_no(self, *args, **kwargs):
        return True


verify_code_sms = VerifyCodeSMS()
