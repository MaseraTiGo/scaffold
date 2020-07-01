# coding=UTF-8

import random
import json

from support.generator.field.normal import *
from support.generator.field.model import *
from support.simulate.tool.template.base import BaseTemplate


class CustomerTemplate(BaseTemplate):

    def generate(self):
        birthday  = DateHelper().generate(years = 30)
        phone = PhoneHelper().generate()

        return {
            'name': NameHelper().generate(),
            'gender': GenderConstant().generate(),
            'birthday': birthday,
            'id_number': WorkNumberHelper().generate(),
            'phone': phone,
            'email': EmailHelper().generate(),
            'wecaht': phone,
            'qq': QQHelper().generate(),
            'education': EducationConstant().generate(),
        }
