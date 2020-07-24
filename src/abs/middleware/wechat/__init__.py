# coding=UTF-8
from infrastructure.log.base import logger
from abs.middleware.extend.wechat import MiniMch


mini_mch_server = MiniMch('rongmi')


class WechatMiddleware(object):

    def check_sign(self, kwargs):
        return mini_mch_server.check_sign(kwargs)

    def get_app_sign(self, prepay_id):
        return mini_mch_server.get_app_sign(prepay_id)

    def unifiedorder(self, out_trade_no, price, body, trade_type):
        data = mini_mch_server.unifiedorder(out_trade_no, price, body, trade_type)

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

    def unifiedorder_app(self, out_trade_no, price, body):
        return self.unifiedorder(
            out_trade_no,
            price,
            body,
            'APP'
        )


wechat_middleware = WechatMiddleware()
