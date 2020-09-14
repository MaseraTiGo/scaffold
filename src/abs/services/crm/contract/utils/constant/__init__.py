# coding=UTF-8

class ValueSource(object):

    COMPANY = "company"
    CUSTOMER = "customer"
    SYSTEM = "system"

    CHOICES = (
        (COMPANY, "企业填写"),
        (CUSTOMER, "客户填写"),
        (SYSTEM, "系统生成"),
    )

class KeyType(object):

    IMGAGE = "image"
    TEXT = "text"
    OTHER = "other"

    CHOICES = (
        (IMGAGE, "图片"),
        (TEXT, "文本"),
        (OTHER, "其它"),
    )
