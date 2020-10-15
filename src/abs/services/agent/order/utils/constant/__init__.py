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


class PlanStatus(object):

    WAIT_PAY = "wait_pay"
    PAYING = "paying"
    PAID = "paid"

    CHOICES = (
        (WAIT_PAY, "欠缴费"),
        (PAYING, "回款中"),
        (PAID, '已回款'),
    )


class EvaluationTypes(object):
    WAIT_EVALUATION = 'wait_evaluation'
    EVALUATED = 'evaluated'

    CHOICES = ((WAIT_EVALUATION, "待评价"), (EVALUATED, "已评价"))
