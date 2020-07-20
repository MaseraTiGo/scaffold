# coding=UTF-8

import random
from support.common.generator.field.base import BaseHelper


class GenderConstant(BaseHelper):

    def calc(self):
        from abs.middleground.business.person.utils.constant import GenderTypes
        return random.choice(GenderTypes.CHOICES)[0]


class EducationConstant(BaseHelper):

    def calc(self):
        from abs.middleground.business.person.utils.constant import EducationTypes
        return random.choice(EducationTypes.CHOICES)[0]


class PayTypeConstant(BaseHelper):

    def calc(self):
        from abs.middleground.business.transaction.utils.constant import PayTypes
        return random.choice(PayTypes.CHOICES)[0]


class BusinessTypeConstant(BaseHelper):

    def calc(self):
        from abs.middleground.business.transaction.utils.constant import BusinessTypes
        return random.choice(BusinessTypes.CHOICES)[0]


class TransactionStatusConstant(BaseHelper):

    def calc(self):
        from abs.middleground.business.transaction.utils.constant import TransactionStatus
        return random.choice(TransactionStatus.CHOICES)[0]
