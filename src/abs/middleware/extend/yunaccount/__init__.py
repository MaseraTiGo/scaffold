# coding=UTF-8

from .transport import yunaccount_transport


class YunaccountExtend(object):

    def check_sign(self, encry_data, mess, timestamp, check_sign):
        sign = yunaccount_transport.get_sign(encry_data, mess, timestamp)
        return True if sign == check_sign else False

    def get_decrypt(self, encry_data):
        return yunaccount_transport.get_decrypt(encry_data)

    def transfers(self, amount, bankcard, order_sn):
        """打款"""
        result = yunaccount_transport.transfers(
            order_sn,
            bankcard.name,
            bankcard.bank_number,
            bankcard.phone,
            bankcard.identification,
            str(amount/100)
        )
        if result['code'] != "0000":
            print(result)
            return False, result
        return True, result

    def transfers_for_alipay(self, dic_param):
        """支付宝打款"""
        pass

    def verify_identity(self, name, identity):
        """姓名身份证号验证"""
        result = yunaccount_transport.verify_identity(
            name,
            identity
        )
        if result['code'] != "0000":
            return False, result
        return True, result

    def verify_bankcard_three_factor(self, name, identity, card_no):
        """银行三要素"""
        pass

    def verify_bankcard_four_factor(self, name, identity, card_no, phone):
        result = yunaccount_transport.verify_bankcard_four_factor(
            name,
            identity,
            card_no,
            phone
        )
        if result['code'] != "0000":
            return False, result
        return True, result


yunaccount_extend = YunaccountExtend()
