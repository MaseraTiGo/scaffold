# coding=UTF-8

import requests
from infrastructure.core.exception.business_error import BusinessError
from abs.middleware.config import config_middleware


class WechatLogin(object):
    access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={app_id}&secret={secret}&code={code}&' \
                       'grant_type=authorization_code'
    user_info_url = 'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={open_id}'

    @property
    def app_id(self):
        return config_middleware.get_value("wechat_clzj_app", "appid")

    @property
    def app_secret(self):
        return config_middleware.get_value("wechat_clzj_app", "appsecret")

    def login(self, code):
        res = self.get_access_token(code)
        access_token = res.get('access_token')
        open_id = res.get('openid')
        return open_id, access_token

    def get_access_token(self, code):
        params = {
            'app_id': self.app_id,
            'secret': self.app_secret,
            'code': code,
        }
        res = requests.get(self.access_token_url.format(params)).json()
        if res.get('access_token'):
            return res
        raise BusinessError("invalid code")

    def get_user_info(self, access_token, open_id):
        params = {
            'access_token': access_token,
            'open_id': open_id
        }

        user_info = requests.get(self.user_info_url.format(params)).json()
        if not user_info.get('openid'):
            return {}
        return user_info
