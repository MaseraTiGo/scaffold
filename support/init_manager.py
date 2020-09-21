# coding=UTF-8

import init_envt

from infrastructure.utils.common.single import Single
from support.environment.init import CustomerInitializeMaker, \
        CrmInitializeMaker, ControllerInitializeMaker


class InitManager(Single):

    def run(self):
        ControllerInitializeMaker().run()
        # CrmInitializeMaker().run()
        # CustomerInitializeMaker().run()


if __name__ == "__main__":
    InitManager().run()
