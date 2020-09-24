# coding=UTF-8


class CategoryTypes(object):
    WECHAT = 'wechat'
    CHOICES = ((WECHAT, '微信小程序'),)


class LoginSystem(object):
    IOS = 'ios'
    ANDROID = 'android'
    OTHER = 'other'
    CHOICES = ((IOS, 'ios'), (ANDROID, '安卓'), (OTHER, '其它'))
