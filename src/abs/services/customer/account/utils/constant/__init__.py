# coding=UTF-8


class CategoryTypes(object):
    WECHAT = 'wechat'
    WECHAT_APP = 'wechat_app'
    QQ = 'QQ'
    CHOICES = ((WECHAT, '微信小程序'), (WECHAT_APP, "微信app"), (QQ, 'QQ'))


class LoginSystem(object):
    IOS = 'ios'
    ANDROID = 'android'
    OTHER = 'other'
    CHOICES = ((IOS, 'ios'), (ANDROID, '安卓'), (OTHER, '其它'))
