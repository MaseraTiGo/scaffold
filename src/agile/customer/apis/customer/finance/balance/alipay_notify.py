# coding=UTF-8
import datetime
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.log.base import logger
from abs.middleware.pay import pay_middleware
from abs.services.customer.finance.manager import CustomerFinanceServer
from django.http.response import HttpResponse
from abs.services.agent.order.manager import OrderServer


def alipay_top_up_notify(request):
    data = request.POST.copy()
    try:
        if not pay_middleware.alipay_check_sign(data):
            raise BusinessError('支付宝支付回调签名错误，订单号（{out_trade_no}）'.format(
                out_trade_no=data['out_trade_no']
            ))

        pay_time = datetime.datetime.strptime(data['gmt_payment'], '%Y-%m-%d %H:%M:%S')
        order_sn = data['out_trade_no']
        total_amount = int(round(float(data['total_amount']) * 100))
        print(order_sn)
        if data['trade_status'] in ['TRADE_FINISHED', 'TRADE_SUCCESS']:
            CustomerFinanceServer.top_up_notify(
                order_sn,
                pay_time,
                data['trade_no'],
                total_amount
            )
        elif data['trade_status'] == 'TRADE_CLOSED':
            # 交易关闭回调
            pass
        else:
            raise BusinessError('交易状态异常')
        return HttpResponse("SUCCESS")
    except Exception as e:
        logger.error(e.get_msg())
        return HttpResponse("FAIL")


def alipay_order_pay_notify(request):
    data = request.POST.copy()
    try:
        if not pay_middleware.alipay_check_sign(data):
            raise BusinessError('支付宝支付回调签名错误，订单号（{out_trade_no}）'.format(
                out_trade_no=data['out_trade_no']
            ))

        pay_time = datetime.datetime.strptime(data['gmt_payment'], '%Y-%m-%d %H:%M:%S')
        order_sn = data['out_trade_no']

        if data['trade_status'] in ['TRADE_FINISHED', 'TRADE_SUCCESS']:
            OrderServer.pay_success_callback(order_sn)
        elif data['trade_status'] == 'TRADE_CLOSED':
            # 交易关闭回调
            OrderServer.pay_fail_callback(order_sn)
        else:
            raise BusinessError('交易状态异常')
        return HttpResponse("SUCCESS")
    except Exception as e:
        logger.error(e.get_msg())
        return HttpResponse("FAIL")
