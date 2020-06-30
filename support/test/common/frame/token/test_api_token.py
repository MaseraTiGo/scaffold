# coding=UTF-8

import unittest
import json

from abs.service.account.manager import StaffAccountServer
from abs.service.user.manager import UserServer

from model.store.model_user import Staff


class TestUserServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_api_token(self):
        """ test api token"""

        staff = Staff.query()[0]

        print('-------'*10)
        token = UserServer.generate_token(staff)
        print(str(token))

        print('-------'*10)
        token = UserServer.get_token(token.auth_token)
        print(str(token))

        print('-------'*10)
        token = UserServer.renew_token(token.auth_token, token.renew_flag)
        print(str(token))
