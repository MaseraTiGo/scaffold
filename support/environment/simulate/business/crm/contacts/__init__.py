# coding=UTF-8

from support.common.maker import BaseLoader
from support.common.generator.field.normal import *
from support.common.generator.field.model import *


class CrmAgentContactsLoader(BaseLoader):

    def generate(self):
        return {
            'contacts': NameHelper().generate(),
            'gender': GenderConstant().generate(),
            'phone': PhoneHelper().generate(),
            'email': EmailHelper().generate(),
        }
