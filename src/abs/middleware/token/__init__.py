# coding=UTF-8

import hashlib

from abs.middleware.token.token import Token


class TokenManager(object):

    @classmethod
    def generate_token(cls, role, user_id):
        token=Token.generate(role,user_id)
        return token

    @classmethod
    def renew_token(cls, auth_str, renew_str):
        token=Token.get(auth_str)
        token.renew(renew_str)
        return token

    @classmethod
    def get_token(cls, auth_str, parms=None):
        token=Token.get(auth_str)
        token.check(parms)
        return token

    @classmethod
    def clear_token(cls, auth_str):
        token=Token.get(auth_str)
        token.clear()
