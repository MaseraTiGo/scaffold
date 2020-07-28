# coding=UTF-8
import datetime

from django.http.response import HttpResponse
from infrastructure.core.exception.business_error import BusinessError

from abs.middleware.extend.yunaccount import yunaccount_extend
from abs.services.customer.finance.manager import CustomerFinanceServer


def yunaccount_transfer_notify(request):
    back_mapping = request.POST
    if yunaccount_extend.check_sign(
        back_mapping["data"],
        back_mapping["mess"],
        back_mapping["timestamp"],
        back_mapping["sign"]
    ):
        result = yunaccount_extend.get_decrypt(back_mapping["data"])
        data = result['data']
        if data['status'] == '1':
            CustomerFinanceServer.withdraw_success_notify(
                data['order_id']
            )
        elif data['status'] == '4':
            CustomerFinanceServer.withdraw_wait_notify(
                data['order_id']
            )
        else:
            CustomerFinanceServer.withdraw_fail_notify(
                data['order_id']
            )
    else:
        print("====云账户提现签名错误", back_mapping)
    return HttpResponse('success')
