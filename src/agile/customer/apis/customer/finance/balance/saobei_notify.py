# coding=UTF-8
import xmltodict
import datetime
import json
from django.http.response import HttpResponse
from infrastructure.log.base import logger
from infrastructure.core.exception.business_error import BusinessError
from abs.middleware.extend.saobei.saobei import saobei_extend
from abs.services.agent.order.manager import OrderServer


def saobei_order_pay_notify(request):
    notify_result = request.body
    result = json.loads(notify_result.decode("utf-8"))
    try:
        pay_notify_run(result)
        param = {"return_code": "01", "return_msg": "OK"}
    except Exception as e:
        logger.error(e.get_msg())
        param = {"return_code": "02", "return_msg": e.get_msg()}
    return HttpResponse(json.dumps(param, ensure_ascii = False), content_type = "application/json,charset=utf-8")

def check_sign(**param):
    sign_str = ""
    sign_order_str = ["return_code", "return_msg", "result_code", "pay_type", "user_id", \
                      "merchant_name", "merchant_no", "terminal_id", "terminal_trace", "terminal_time", \
                      "total_fee", "end_time", "out_trade_no", "channel_trade_no", "attach"]
    for str in sign_order_str:
        if str in param:
            if sign_str == "":
                sign_str = "{sign_str}{key}={value}".format(sign_str = sign_str, key = str, value = param[str])
            else:
                sign_str = "{sign_str}&{key}={value}".format(sign_str = sign_str, key = str, value = param[str])

    sign = saobei_extend.get_sign(sign_str)
    if sign == param["key_sign"]:
        return True
    return False

def pay_notify_run(data):
    if data['return_code'] != '01' or data['result_code'] != '01':
        raise BusinessError('支付回调失败，订单号（{terminal_trace}），错误描述：{return_msg}'\
                            .format(terminal_trace = data['terminal_trace'], return_msg = data['return_msg']))
        if  data['result_code'] == '02':
            # 交易关闭回调
            OrderServer.pay_fail_callback(order_sn)
    if not check_sign(**data):
        raise BusinessError('支付回调验签失败，订单号（{terminal_trace}）'.format(terminal_trace = data['terminal_trace']))
    pay_time = datetime.datetime.strptime(data['end_time'], '%Y%m%d%H%M%S')
    order_sn = data['terminal_trace']
    OrderServer.pay_success_callback(order_sn)

    return True

