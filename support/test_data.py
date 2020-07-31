# coding=UTF-8

import init_envt

from infrastructure.utils.common.single import Single
from support.environment.simulate import CrmSimulateMaker, \
        CustomerSimulateMaker


class TestDataManager(Single):

    def run(self):
        # generate staff
        CrmSimulateMaker().run(1)

        # generate customer by staff
        CustomerSimulateMaker().run(1)


if __name__ == "__main__":
    TestDataManager().run()
