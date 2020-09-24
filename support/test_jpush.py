# coding=UTF-8

import init_envt

from infrastructure.utils.common.single import Single
from abs.middleware.extend.jpush import jpush_extend


class TestJpush(Single):

    def run(self):
        print("===>12123312312123")
        # generate staff
        jpush_extend.alias()


if __name__ == "__main__":
    TestJpush().run()
