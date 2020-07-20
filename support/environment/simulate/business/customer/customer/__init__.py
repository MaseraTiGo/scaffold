# coding=UTF-8

from support.common.generator.field.normal import \
        NameHelper, DateHelper, PhoneHelper, EmailHelper,\
        QQHelper
from support.common.generator.field.model import GenderConstant
from support.common.maker import BaseLoader


class CustomerLoader(BaseLoader):

    def generate(self):
        birthday = DateHelper().generate(years=30)
        phone = PhoneHelper().generate()

        return {
            'name': NameHelper().generate(),
            'gender': GenderConstant().generate(),
            'birthday': birthday,
            'phone': phone,
            'email': EmailHelper().generate(),
            'wecaht': phone,
            'qq': QQHelper().generate(),
        }
