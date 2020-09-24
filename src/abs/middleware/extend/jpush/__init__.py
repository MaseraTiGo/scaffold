# coding=UTF-8

import jpush as jpush


class JpushExtend(object):

    app_key = 'f49ba8db36ec204fbaca066b'
    master_secret = '7d2984b05ac1a7340f803e88'
    _jpush = jpush.JPush(app_key, master_secret)
    _jpush.set_logging("DEBUG")

    def all(self):
        push = self._jpush.create_push()
        push.audience = jpush.all_
        push.notification = jpush.notification(alert = "nihaoma")
        push.platform = jpush.all_
        try:
            response = push.send()
            print("==>>>>response", response, type(response))
        except:
            print("Exception")

    def alias(self):
        push = self._jpush.create_push()
        alias = ["6B9F14DF9B5847E5A8C7C2D708A00885"]
        alias1 = {"alias": alias}
        push.audience = jpush.audience(
            alias1
        )
        android_msg = jpush.android(
            alert = "尊敬的《橙鹿教育》用户，您好，感谢您的支持和信任，特意提醒，您有一份待签署的合同，立即前往签署>>",
            title = "提醒：您有一份待签署的合同",
            extras = {"type":"contract", "id":"1"}
        )
        ios_msg = jpush.ios(
            alert = {"title":"提醒：您有一份待签署的合同",
                     "body":"尊敬的《橙鹿教育》用户，您好，感谢您的支持和信任，特意提醒，您有一份待签署的合同，立即前往签署>>"},
            extras = {"type":"contract", "id":"1"}
        )
        push.notification = jpush.notification(
            # android = android_msg,
            ios = ios_msg
        )
        push.options = {"apns_production":False}
        push.platform = jpush.all_
        push.send()

jpush_extend = JpushExtend()
