# coding=UTF-8


class OrderStatus(object):

    ORDER_LAUNCHED = "order_launched"
    PAYMENT_FINISHED = "payment_finished"
    DELIVERY_FINISHED = "delivery_finished"
    ORDER_CLOSED = "order_closed"  # 发货前的终结操作
    ORDER_FINISHED = "order_finished"  # 发货后的终结操作

    CHOICES = (
        (ORDER_LAUNCHED, "订单已下单"),
        (PAYMENT_FINISHED, "订单支已支付"),
        (DELIVERY_FINISHED, "订单已发货"),
        (ORDER_CLOSED, "订单关闭"),
        (ORDER_FINISHED, "订单完成"),
    )
