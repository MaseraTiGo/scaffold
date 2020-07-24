# coding=UTF-8


class DespatchService(object):
    LOGISTICS = "logistics"
    OFFLINE = "offline"
    ONLINE = "online"
    CHOICES = (
        (LOGISTICS, '物流交付'),
        (OFFLINE, "线下交付"),
        (ONLINE, "线上交付"),
    )


class UseStatus(object):
    ENABLE = "enable"
    FORBIDDENT = "forbiddent"
    CHOICES = (
        (ENABLE, '启用'),
        (FORBIDDENT, "禁用"),
    )
