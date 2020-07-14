# coding=UTF-8


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
