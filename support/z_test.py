# coding=UTF-8

import init_envt

from infrastructure.utils.common.single import Single
from abs.middleware.image import image_middleware


class TmpTest(Single):

    def run(self):
        image_middleware.get_contract()

if __name__ == "__main__":
    TmpTest().run()
