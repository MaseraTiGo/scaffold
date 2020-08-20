# coding=UTF-8


class TrackTypes(object):
    PHONE = "phone"
    WECHAT = "wechat"
    MESSAGE = 'message'
    EMAIL = 'email'
    OTHER = "other"
    CHOICES = ((PHONE, '电话'), (WECHAT, "微信"), (MESSAGE, "短信"), \
               (EMAIL, "邮件"), (OTHER, "其它"))