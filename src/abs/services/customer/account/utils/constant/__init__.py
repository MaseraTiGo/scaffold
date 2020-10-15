# coding=UTF-8


class CategoryTypes(object):
    WECHAT = 'wechat'
    WECHAT_APP = 'wechat_app'
    CHOICES = ((WECHAT, '微信小程序'), (WECHAT_APP, "微信app"))


class LoginSystem(object):
    IOS = 'ios'
    ANDROID = 'android'
    OTHER = 'other'
    CHOICES = ((IOS, 'ios'), (ANDROID, '安卓'), (OTHER, '其它'))
