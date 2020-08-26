# coding=UTF-8


class OrderSource(object):

    APP = "app"
    CRM = "crm"
    WECHAT = 'wechat'
    OTHER = "other"

    CHOICES = (
        (APP, "app"),
        (CRM, "crm"),
        (WECHAT, 'wechat'),
        (OTHER, "other"),
    )
