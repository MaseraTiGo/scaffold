# coding=UTF-8

from abs.middleware.extend.alipay import alipay_extend


class AlipayMiddleware(object):

    def get_app_top_up_info(self, input_record):
        notify_path = '/interface/'
        result_str = alipay_extend.get_order_info(
            '充值',
            '充值',
            input_record.number,
            str(input_record.amount/100),
            notify_path
        )
        return result_str


alipay_middleware = AlipayMiddleware()
