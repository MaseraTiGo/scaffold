# coding=UTF-8


class DespatchService(object):
    LOGISTICS = "logistics"
    TOP_UP_PHONE = "phone_top_up"
    EDUCTION_CONTRACT = "eduction_contract"
    CHOICES = (
        (LOGISTICS, '物流交付'),
        (TOP_UP_PHONE, "手机充值"),
        (EDUCTION_CONTRACT, "教育合同"),
    )


class DespatchInformation(object):
    LOGISTICS = ('name', 'address', 'phone')
    TOP_UP_PHONE = ('phone',)
    EDUCTION_CONTRACT = ('name', 'phone', 'identification')
    CHOICES = (
        (LOGISTICS, '物流交付基础属性'),
        (TOP_UP_PHONE, "手机充值基础属性"),
        (EDUCTION_CONTRACT, "教育合同基础属性"),
    )


class UseStatus(object):
    ENABLE = "enable"
    FORBIDDENT = "forbiddent"
    CHOICES = (
        (ENABLE, '启用'),
        (FORBIDDENT, "禁用"),
    )
