# coding=UTF-8

import random
from support.generator.field.base import BaseHelper


class GenderConstant(BaseHelper):

    def calc(self):
        from model.common.model_user_base import GenderTypes
        return random.choice(GenderTypes.CHOICES)[0]


class EducationConstant(BaseHelper):

    def calc(self):
        from model.common.model_user_base import EducationType
        return random.choice(EducationType.CHOICES)[0]


class PayTypeConstant(BaseHelper):

    def calc(self):
        from model.store.model_customer import PayTypes
        return random.choice(PayTypes.CHOICES)[0]


class BusinessTypeConstant(BaseHelper):

    def calc(self):
        from model.store.model_customer import BusinessTypes
        return random.choice(BusinessTypes.CHOICES)[0]


class TransactionStatusConstant(BaseHelper):

    def calc(self):
        from model.store.model_customer import TransactionStatus
        return random.choice(TransactionStatus.CHOICES)[0]
