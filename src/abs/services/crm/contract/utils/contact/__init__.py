# coding=UTF-8

class ValueSource(object):

    INVOICE = "invoice"
    AGENT = "agent"
    OTHER = "other"

    CHOICES = (
        (INVOICE, "发货单"),
        (AGENT, "代理商"),
        (OTHER, "其它"),
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
