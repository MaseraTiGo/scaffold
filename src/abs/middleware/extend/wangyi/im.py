# coding=UTF-8

import time
import json
import hashlib
import requests
import random


class ImExtend(object):


    def __init__(self):
        self._ContentType = "application/x-www-form-urlencoded;charset=utf-8"

    def get_appkey(self):
        return  # "29c0d0c46bf2c6fd49c2fe9d5f35ac84"  # 请求连接

    def get_appsecret(self):
        return  # "d828ece10671"  # 请求连接

    def get_fromal_url(self):
        return  "https://api.netease.im/nimserver/"  # 请求连接

    def _get_current_time(self):
        return int(time.time())

    def _get_random_number(self):
        return random.randint(1000000000, 9999999999)

    def _get_headers(self):
        str_time = str(self._get_current_time())
        str_noce = str(self._get_random_number())
        str_header = "{appsecret}{noce}{curtime}".format(appsecret = self.get_appsecret(), \
                                                         noce = str_noce, \
                                                         curtime = str_time).encode(encoding = 'utf_8')
        checksum = hashlib.sha1(str_header).hexdigest()
        return {'content-type': self._ContentType, "appKey": self.get_appkey(), \
                "nonce": str_noce, "curTime": str_time, "CheckSum":checksum}


    def _request_api(self, url, **param):
        url = "{baseurl}{url}".format(baseurl = self.get_fromal_url(), url = url)
        result = requests.post(url, data = json.dumps(param), headers = self._get_headers())
        result_str = result.content
        result_data = json.loads(result_str.decode("utf-8"))
        return result_data

    def create(self, dic_param):
        """创建通信ID"""
        url = "user/create.action"
        param = {
                 "accid":dic_param["accid"],  # 网易云通信ID，最大长度32字符，必须保证一个APP内唯一（只允许字母、数字、半角下划线_、@、半角点以及半角-组成，不区分大小写，会统一小写处理，请注意以此接口返回结果中的accid为准）。
                 # "name":"",  # 网易云通信ID昵称，最大长度64字符（非必填字段）
                 # "icon":"",  # 网易云通信ID头像URL，开发者可选填，最大长度1024（非必填字段）
                 # "token":"",  # 网易云通信ID可以指定登录token值，最大长度128字符，并更新，如果未指定，会自动生成token，并在创建成功后返回（非必填字段）
                 # "sign":"",  # 用户签名，最大长度256字符（非必填字段）
                 # "email":"",  # 用户email，最大长度64字符（非必填字段）
                 # "birth":"",  # 用户生日，最大长度16字符（非必填字段）
                 # "mobile":"",  # 用户手机号（非必填字段）
                 # "gender":"",  # 用户性别，0表示未知，1表示男，2女表示女，其它会报参数错误（非必填字段）
                 # "ex":""  # 用户名片扩展字段，最大长度1024字符，用户可自行扩展，建议封装成JSON字符串（非必填字段）
                 }
        return self._request_api(url, **param)

    def get_history_message(self, dic_param):
        """获取单聊云端历史消息"""
        url = "history/querySessionMsg.action"
        param = {
               "from":dic_param["from"],  # 发送者accid
               "to":dic_param["to"],  # 接收者accid
               "begintime":dic_param["begintime"],  # 开始时间，毫秒级
               "endtime":dic_param["endtime"],  # 截至时间毫秒级
               "limit":dic_param["limit"],  # 本次查询的消息条数上限（最多100条），小于等于0，或者大于100，会提示参数错误
               # "reverse":"",  # （非必填字段）1按时间正序排列，2按时间降序排列。
               # "type":""  # （非必填字段）查询指定的多个消息类型，类型之间用","分割，不设置该参数则查询全部类型消息格式示例： 0,1,2,3 类型支持： 1:图片，2:语音，3:视频，4:地理位置，5:通知，6:文件，10:提示，11:Robot，100:自定义
               }
        return self._request_api(url, **param)


im_extend = ImExtend()
