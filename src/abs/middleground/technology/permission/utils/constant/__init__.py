# coding=UTF-8


class PermissionTypes(object):

    POSITION = "position"
    PERSON = "person"

    CHOICES = (
        (POSITION, "身份权限"),
        (PERSON, "个人权限"),
    )


class UseStatus(object):

    ENABLE = "enable"
    FORBIDDEN = "forbidden"

    CHOICES = (
        (ENABLE, "启动"),
        (FORBIDDEN, "禁用"),
    )
