# coding=UTF-8


class OperationTypes(object):
    VISIT = "visit"
    INTENTION = "intention"
    CUSTOMER = 'customer'
    OTHER = "other"
    CHOICES = ((VISIT, '添加访问记录'), (INTENTION, "意向修改"), \
               (CUSTOMER, "客户信息修改"), (OTHER, "其它"))