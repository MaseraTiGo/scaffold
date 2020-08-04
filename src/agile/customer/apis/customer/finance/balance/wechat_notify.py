# coding=UTF-8
import xmltodict
import datetime
from django.http.response import HttpResponse
from infrastructure.log.base import logger
from infrastructure.core.exception.business_error import BusinessError
from abs.services.customer.finance.manager import CustomerFinanceServer
from abs.middleware.pay import pay_middleware
from abs.middleground.business.order.manager import OrderServer as mg_OrderServer


def wechat_top_up_notify(request):
    xml_body = request.body
    data = xmltodict.parse(xml_body)['xml']
    try:
        if data['return_code'] != 'SUCCESS':
            raise BusinessError(
                '支付回调失败，{return_msg}'.format(
                    return_msg=data['return_msg']
                )
            )
        if data['result_code'] != 'SUCCESS':
            raise BusinessError(
                '支付回调失败，订单号（{out_trade_no}），错误代码：{err_code}，错误描述：{err_code_des}'.format(
                    out_trade_no=data['out_trade_no'],
                    err_code=data['err_code'],
                    err_code_des=data['err_code_des']
                )
            )
        if not pay_middleware.check_sign(data):
            raise BusinessError('支付回调签名错误，订单号（{out_trade_no}）'.format(
                out_trade_no=data['out_trade_no']
            ))

        pay_time = datetime.datetime.strptime(data['time_end'], '%Y%m%d%H%M%S')
        order_sn = data['out_trade_no']

        CustomerFinanceServer.top_up_notify(
            order_sn,
            pay_time,
            data['transaction_id'],
            data['total_fee']
        )
        return success_response()
    except Exception as e:
        logger.error(e.get_msg())
        return fail_response(e.get_msg())


def wechat_order_pay_notify(request):
    xml_body = request.body
    data = xmltodict.parse(xml_body)['xml']
    try:
        if data['return_code'] != 'SUCCESS':
            raise BusinessError(
                '支付回调失败，{return_msg}'.format(
                    return_msg=data['return_msg']
                )
            )
        if data['result_code'] != 'SUCCESS':
            raise BusinessError(
                '支付回调失败，订单号（{out_trade_no}），错误代码：{err_code}，错误描述：{err_code_des}'.format(
                    out_trade_no=data['out_trade_no'],
                    err_code=data['err_code'],
                    err_code_des=data['err_code_des']
                )
            )
        if not pay_middleware.check_sign(data):
            raise BusinessError('支付回调签名错误，订单号（{out_trade_no}）'.format(
                out_trade_no=data['out_trade_no']
            ))

        pay_time = datetime.datetime.strptime(data['time_end'], '%Y%m%d%H%M%S')
        order_sn = data['out_trade_no']
        mg_OrderServer.pay_success_callback(order_sn)

        return success_response()
    except Exception as e:
        logger.error(e.get_msg())
        return fail_response(e.get_msg())


def fail_response(msg):
    param = {'root': {'return_code': 'FAIL', 'return_msg': msg}}
    return HttpResponse(xmltodict.unparse(param))


def success_response():
    param = {'root': {'return_code': 'SUCCESS', 'return_msg': 'OK'}}
    return HttpResponse(xmltodict.unparse(param))
