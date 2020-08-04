# coding=UTF-8

from infrastructure.log.base import logger
from abs.middleware.extend.wechat import MiniMch

from abs.middleware.extend.alipay import alipay_extend

mini_mch_server = MiniMch('rongmi')


class PayMiddleware(object):

    def get_prepay_id(
        self,
        pay_type,
        number,
        amount,
        notify_path,
        body,
        trade_type=''
    ):
        prepay_id = ''
        if pay_type == 'wechat':
            data = mini_mch_server.unifiedorder(
                number,
                amount,
                notify_path,
                body=body,
                trade_type=trade_type
            )
            result = self.wechat_handle(data, number)
            if result:
                prepay_id = result['prepay_id']
        elif pay_type == 'alipay':
            prepay_id = alipay_extend.get_order_info(
                number,
                str(amount / 100),
                notify_path,
                body,
                body
            )
        return prepay_id

    def top_up(self, pay_type, number, amount, trade_type='APP'):
        notify_path = ''
        if pay_type == 'wechat':
            notify_path = '/interface/wechat_top_up_notify'
        elif pay_type == 'alipay':
            notify_path = '/interface/alipay_top_up_notify'

        prepay_id = self.get_prepay_id(
            pay_type,
            number,
            amount,
            notify_path,
            body='充值',
            trade_type=trade_type
        )
        return prepay_id

    def pay_order(self, pay_type, number, amount, trade_type='APP'):
        notify_path = ''
        if pay_type == 'wechat':
            notify_path = '/interface/wechat_pay_order_notify'
        elif pay_type == 'alipay':
            notify_path = '/interface/alipay_pay_order_notify'

        prepay_id = self.get_prepay_id(
            pay_type,
            number,
            amount,
            notify_path,
            body='订单付款',
            trade_type=trade_type
        )
        return prepay_id

    def parse_pay_info(cls, prepay_id, pay_type):
        pay_info = {
            'timestamp': '',
            'prepayid': prepay_id,
            'noncestr': '',
            'sign': ''
        }
        if pay_type == 'wechat':
            pay_info = mini_mch_server.get_app_sign(prepay_id)
            pay_info.update({
                'timestamp': pay_info.get('timestamp'),
                'prepayid': pay_info.get('prepayid'),
                'noncestr': pay_info.get('noncestr'),
                'sign': pay_info.get('sign')
            })
        return pay_info

    def wechat_handle(self, data, out_trade_no):
        if data.get('return_code') != 'SUCCESS':
            logger.error('统一下单接口调用失败，订单号（{out_trade_no}），{return_msg}'.format(
                out_trade_no=out_trade_no,
                return_msg=data['return_msg']
            ))
            return None

        if data.get('result_code') != 'SUCCESS':
            logger.error(
                '统一下单接口调用失败，订单号（{out_trade_no}），错误代码：{err_code}，错误描述：{err_code_des}'.format(
                    out_trade_no=out_trade_no,
                    err_code=data['err_code'],
                    err_code_des=data['err_code_des'])
            )
            return None
        return data

    def wechant_check_sign(self, kwargs):
        return mini_mch_server.check_sign(kwargs)


pay_middleware = PayMiddleware()