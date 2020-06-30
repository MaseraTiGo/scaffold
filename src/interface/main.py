# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

import json
import hashlib
import itertools
import xml.sax

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import infrastructure.utils.common.signature as signature
from infrastructure.core.api.doc import TextApiDoc
from infrastructure.core.exception.api_error import api_errors
from infrastructure.core.exception.pro_error import pro_errors
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.core.exception.system_error import SysError
from infrastructure.log.base import logger

from agile.base.protocol.django import DjangoProtocol
from agile.crm.manager.server import crm_pc_service
from agile.customer.manager.server import customer_mobile_service
from agile.file.manager.server import file_service
from abs.middleware.rule import rule_register
from abs.middleware.xml import XMLHandler

protocol = DjangoProtocol()
protocol.add(crm_pc_service)
protocol.add(file_service)
protocol.add(customer_mobile_service)


def router(request):
    result = protocol.run(request)
    resp = HttpResponse(json.dumps(result))
    resp['Access-Control-Allow-Origin'] = '*'  # 处理跨域请求
    return resp


def api_doc(request):
    api_signature_doc = signature.__doc__
    services = protocol.get_services()
    for service in services:
        apis = service.get_apis()
        service.api_docs = [TextApiDoc(api) for api in apis]

    error_list = []
    error_list.append(SysError)
    error_list.extend(pro_errors.get_errors())
    error_list.extend(api_errors.get_errors())
    error_list.append(BusinessError)
    error_list = [(err.get_flag(), err.get_code(), err.get_desc()) for err in error_list]

    return render(request, 'api_index.html', {
        'api_signature_doc': api_signature_doc,
        'services': services,
        'error_list': error_list,
    })


def premise_doc(request):
    rule_roots = rule_register.get_roots()
    return render('premise_index.html', {
        'root_list': rule_roots
    })


def access_token(request):
    token = 'fantastic'
    if request.method == 'GET':
        code = request.GET.get('code', '')
        if code:
            # get user's open_id
            url_redirect = request.GET.get('url', '')
            url_part = request.path.split('/')[-1]
            open_id, merchant_sn, app_id = WeChatServer.authorized_load(url_part, code)
            if not open_id:
                return HttpResponseRedirect(url_redirect)
            parms = {'open_id': open_id, 'app_id': app_id, 'merchant_sn': merchant_sn}
            parms_str = '&'.join(["{}={}".format(key, val) for key, val in parms.items()])
            full_url = "{}?{}".format(url_redirect, parms_str)
            return HttpResponseRedirect(full_url)  # this redirect url just for testing
        else:
            # checkout server info
            signature = request.GET['signature']
            timestamp = request.GET['timestamp']
            nonce = request.GET['nonce']
            echostr = request.GET['echostr']
            temp_str = ''.join(sorted((token, timestamp, nonce)))
            temp_str = temp_str.encode('utf-8')
            signature_gen = hashlib.sha1(temp_str).hexdigest()
            if signature_gen == signature:
                return HttpResponse(echostr)
            else:
                return HttpResponse('error')
    if request.method == 'POST':
        code = request.GET.get('code', '')
        # return HttpResponse('')
        url_part = request.path.split('/')[-1]
        if code:
            # get user's open_id
            WeChatServer.authorized_load(url_part, code)
            return HttpResponse('success')
        else:
            xml_data = request.body.decode('utf-8')
            # avoid to return error info , so use the async
            import threading
            t = threading.Thread(target = msg_reply, args = (xml_data, url_part))
            t.start()
            t.join()
            return HttpResponse('')


def msg_reply(xml_data, url_part):
    # process user's post info
    xml_data = xml_data.replace(' ', '')
    xml_data = xml_data.strip('\n')
    xh = XMLHandler()
    xml.sax.parseString(xml_data.encode('utf-8'), xh)
    ret = xh.getDict()
    ret['URL'] = url_part
    # try:
    WeChatServer.msg_auto_reply(ret)
    # except Exception as e:
    #     print('--------------->exception happened!', e)
