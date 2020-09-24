# coding=UTF-8


import jpush as jpush
from api.utils import utils_url
from common import web_helper


@utils_url.route('/xxx', methods = ['post'])
def tuisong_message():
    content_ = "你好吗"  # 推送内容

    # app_key和master_secret
    app_key = 'xxx'
    master_secret = 'xxx'

    _jpush = jpush.JPush(app_key, master_secret)
    push = _jpush.create_push()
    push.audience = jpush.all_
    push.notification = jpush.notification(alert = content_)
    push.platform = jpush.all_
    try:
        res = push.send()
    except Exception:
        print('推送失败')
    print('推送成功')

jpush_extend = JpushExtend()
