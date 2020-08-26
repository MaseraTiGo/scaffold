# coding=UTF-8


class StatusTypes(object):
    SUCCESS='success'
    FAIL='fail'
    RESEND='resend'
    CHOICES=((SUCCESS,'成功'),(FAIL,"失败"),(RESEND,"已重发"))


class SourceTypes(object):
    CRM='crm'
    CUSTOMER='customer'
    CUSTOMER_WECHAT='customer_wechat'
    CHOICES=((CRM,'crm'),(CUSTOMER,'客户端'),(CUSTOMER_WECHAT, '客户端微信小程序'))


class SceneTypes(object):
    REGISTER='register'
    FORGET='forget'
    BINDCARD='bindcard'
    LOGIN = 'login'
    WECHAT_REGISTER = 'wechat_register'
    CHOICES=((REGISTER,'注册验证码'),(FORGET,'找回密码验证码'),
             (BINDCARD,'绑定银行卡'),(LOGIN, '登陆'),
             (WECHAT_REGISTER, '微信注册验证码'))
