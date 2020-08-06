# coding=UTF-8


class PlatformTypes(object):

    CRM = 'crm'
    CUSTOMER = 'customer'
    CONTROLLER = 'controller'
    AGENT = 'agent'

    CHOICES = (
        (CRM, '客户管理系统'),
        (CUSTOMER, '客户端'),
        (CONTROLLER, '中台管控端'),
        (AGENT, '代理商管理系统'),
    )


class StatusTypes(object):

    ENABLE = 'enable'
    LOCK = 'lock'
    DISABLE = 'disable'
    NOTACTIVE = 'notactive'

    CHOICES = (
        (ENABLE, '启用'),
        (NOTACTIVE, '待激活'),
        (LOCK, "锁定"),
        (DISABLE, "禁用")
    )
