# coding=UTF-8

import jpush as jpush
from abs.middleware.config import config_middleware


class JpushExtend(object):

    def get_app_key(self):
        return config_middleware.get_value("jpush", "app_key")

    def get_master_secret(self):
        return  config_middleware.get_value("jpush", "master_secret")

    def alias(self):
        _jpush = self._init()
        push = _jpush.create_push()
        alias = ["246f7ab91c9313c209595cc209b4d1cef"]
        push.audience = jpush.audience(
            {"alias": alias}
        )
        android_msg = jpush.android(
            alert = "尊敬的《橙鹿教育》用户，您好，感谢您的支持和信任，特意提醒，您有一份待签署的合同，立即前往签署>>",
            title = "提醒：您有一份待签署的合同",
            extras = {"type":"contract", "id":"1"}
        )
        ios_msg = jpush.ios(
            alert = {"title":"提醒：您有一份待签署的合同",
                     "body":"1111111"},
            extras = {"type":"contract", "id":"1"}
        )
        push.notification = jpush.notification(
            android = android_msg,
            # ios = ios_msg
        )
        push.options = {"apns_production":False}
        push.platform = jpush.all_

        result = push.send()
        print("==>>>>>result", result, type(result), result.payload, type(result.payload))


    def _init(self):
        _jpush = jpush.JPush(
            self.get_app_key(),
            self.get_master_secret()
        )
        _jpush.set_logging("DEBUG")
        return _jpush

    def alias_send(self, platform, alias, title, content, extras):
        _jpush = self._init()
        push = _jpush.create_push()
        push.audience = jpush.audience(
            {"alias": alias}
        )
        if platform == "android":
            android_msg = jpush.android(
                alert = content,
                title = title,
                extras = extras
            )
            push.notification = jpush.notification(
                android = android_msg,
            )
        elif platform == "ios":
            ios_msg = jpush.ios(
                alert = {"title":title,
                         "body":content},
                extras = extras
            )
            push.notification = jpush.notification(
                ios = ios_msg
            )
            push.options = {"apns_production":False}
        else:
            return False
        push.platform = jpush.all_
        try:
           result = push.send()

        except Exception as e:
            return False
        return True


jpush_extend = JpushExtend()
