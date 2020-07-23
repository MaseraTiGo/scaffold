# coding=UTF-8


class StatusTypes(object):
    SUCCESS = 'success'
    FAIL = 'fail'
    RESEND = 'resend'
    CHOICES = ((SUCCESS, '成功'), (FAIL, "失败"), (RESEND, "已重发"))


class SourceTypes(object):
    CRM = 'crm'
    CUSTOMER = 'customer'
    CHOICES = ((CRM, 'crm'), (CUSTOMER, '客户端'))


class SceneTypes(object):
    REGISTER = 'register'
    CHOICES = ((REGISTER, '注册验证码'), )
