# coding=UTF-8


class LogisticsCompany(object):

    SHUNFENG = "shunfeng"
    YUNDA = "yunda"
    ZHONGTONG = "zhongtong"
    DEBANG = "debang"

    CHOICES = (
        (SHUNFENG, '顺风'),
        (YUNDA, "韵达"),
        (ZHONGTONG, "中通"),
        (DEBANG, "德邦"),
    )


class LogisticsStatus(object):

    PERPARE = "prepare"
    IN_TRANSIT = "in_transit"
    DELIVERY = "delivery"
    LOST = "lost"
    RETURN = "return"

    CHOICES = (
        (PERPARE, '待发货'),
        (IN_TRANSIT, '运输中'),
        (DELIVERY, '交付完成'),
        (LOST, '货物丢失'),
        (RETURN, '货品返回'),
    )
