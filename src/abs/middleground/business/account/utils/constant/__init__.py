# coding=UTF-8


class PlatformTypes(object):

    CRM = 'crm'
    CUSTOMER = 'customer'
    CONTROLLER = 'controller'

    CHOICES = (
        (CRM, '客户管理系统'),
        (CUSTOMER, '客户端'),
        (CONTROLLER, '中台管控端'),
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
