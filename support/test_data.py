# coding=UTF-8

import init_envt

from infrastructure.utils.common.single import Single
from support.environment.simulate import CrmSimulateMaker


class TestDataManager(Single):

    def run(self):
        # generate staff
        CrmSimulateMaker().run(10)

        # generate product
        # ProductMaker().run(1)

        # generate storage
        # StorageMaker().run(1000)

        # generate mobilephone
        # MobileDevicesMaker().run(10)

        # generate customer by staff
        # CustomerMaker().run(10)


if __name__ == "__main__":
    TestDataManager().run()
