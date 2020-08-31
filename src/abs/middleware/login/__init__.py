# coding=UTF-8
from abs.middleware.extend.wechat import Mini
from infrastructure.core.exception.business_error import BusinessError

mini_server = Mini()


class LoginMiddleware(object):

    def wechat_login(self, code):
        res = mini_server.login(code)
        if res.get('openid'):
            return res
        raise BusinessError('登陆异常')

    def get_wechat_info(self, encrypted_data, session_key, iv):
        result = mini_server.get_info(encrypted_data, session_key, iv)
        if result['watermark']['appid'] != mini_server.appid:
            raise BusinessError('微信数据异常')
        return result


login_middleware = LoginMiddleware()
