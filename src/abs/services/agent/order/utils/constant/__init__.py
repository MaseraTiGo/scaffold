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


class ContractStatus(object):

    WAIT_SEND = "wait_send"
    WAIT_SIGNED = "wait_signed"
    SIGNED = 'signed'

    CHOICES = (
        (WAIT_SEND, "待发送"),
        (WAIT_SIGNED, "待签署"),
        (SIGNED, '已签署'),
    )