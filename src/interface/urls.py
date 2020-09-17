# coding=UTF-8

"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from interface.main import router, api_doc, premise_doc, access_token, \
                           app_router, app_api_doc
from agile.customer.apis.customer.finance.balance.wechat_notify import wechat_top_up_notify, \
    wechat_order_pay_notify
from agile.customer.apis.customer.finance.balance.yunaccount_notify import yunaccount_transfer_notify
from agile.customer.apis.customer.finance.balance.alipay_notify import alipay_top_up_notify, alipay_order_pay_notify
from agile.customer.apis.customer.finance.balance.saobei_notify import saobei_order_pay_notify

urlpatterns = [
    url(r'app_api_doc', app_api_doc),
    url(r'api_doc', api_doc),
    url(r'premise_doc', premise_doc),
    url(r'access_token/[0-9]{10}', access_token),
    url(r'^$', router),
    url(r'wechat_top_up_notify', wechat_top_up_notify),
    url(r'alipay_top_up_notify', alipay_top_up_notify),
    url(r'yunaccount_transfer_notify', yunaccount_transfer_notify),
    url(r'wechat_order_pay_notify', wechat_order_pay_notify),
    url(r'alipay_order_pay_notify', alipay_order_pay_notify),
    url(r'saobei_order_pay_notify', saobei_order_pay_notify),
    url(r'app_router', app_router),

]
