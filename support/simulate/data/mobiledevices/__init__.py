# coding=UTF-8

from support.generator.helper import *
from support.simulate.data.base import BaseMaker

from support.simulate.tool.template.mobile import *


class MobileDevicesMaker(BaseMaker):

    def generate_relate(self, mobiledevices_generator, mobilephone_generator, mobilemaintain_generator):
        mobilephone_generator.add_inputs(mobiledevices_generator)
        mobilemaintain_generator.add_inputs(mobiledevices_generator)
        return mobiledevices_generator

    def generate(self):
        mobiledevices = MobileDevicesGenerator(MobileDevicesTemplate().generate())
        mobilephone = MobilePhoneGenerator(MobilePhoneTemplate().generate())
        mobilemaintain = MobileMaintainGenerator(MobileMaintainTemplate().generate())

        mobiledevices_generator = self.generate_relate(mobiledevices, mobilephone, mobilemaintain)
        mobiledevices_generator.generate()
        return mobiledevices_generator
