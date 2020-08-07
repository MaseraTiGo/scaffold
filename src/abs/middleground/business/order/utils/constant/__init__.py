# coding=UTF-8


class OrderStatus(object):

    ORDER_LAUNCHED = "order_launched"
    PAYMENT_FINISHED = "payment_finished"
    DELIVERY_FINISHED = "delivery_finished"
    ORDER_CLOSED = "order_closed"  # 发货前的终结操作
    ORDER_FINISHED = "order_finished"  # 发货后的终结操作

    CHOICES = (
        (ORDER_LAUNCHED, "待支付"),
        (PAYMENT_FINISHED, "待发货"),
        (DELIVERY_FINISHED, "已发货"),
        (ORDER_CLOSED, "已取消"),
        (ORDER_FINISHED, "已完成"),
    )
