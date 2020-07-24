# coding=UTF-8


class OwnTypes(object):
    COMPANY = "company"
    PERSON = "person"
    CHOICES = ((COMPANY, '公司'), (PERSON, "个人"))


class AccountTypes(object):
    EXPEND = "expense"
    INCOME = "income"
    CHOICES = ((EXPEND, '支出'), (INCOME, "收入"))


class PayTypes(object):
    BANK = "bank"
    ALIPAY = "alipay"
    WECHAT = "wechat"
    BALANCE = "balance"
    CHOICES = ((BANK, '银行'), (ALIPAY, "支付宝"), (WECHAT, "微信"), (BALANCE, "余额"))


class BusinessTypes(object):
    ORDER = "order"
    BALANCE = "balance"
    CHOICES = ((ORDER, '订单'), (BALANCE, "余额"))


class TransactionStatus(object):
    PAY_FINISH = "pay_finish"
    TRANSACTION_DEALING = "transaction_dealing"
    ACCOUNT_FINISH = "account_finish"
    ACCOUNT_FAIL = 'account_fail'
    CHOICES = (
        (PAY_FINISH, '付款成功'),
        (TRANSACTION_DEALING, "交易处理中"),
        (ACCOUNT_FINISH, "到账成功"),
        (ACCOUNT_FAIL, "交易失败")
    )
