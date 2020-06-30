# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from infrastructure.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField
from infrastructure.core.api.utils import with_metaclass
from infrastructure.core.api.request import RequestField, RequestFieldSet
from infrastructure.core.api.response import ResponseField, ResponseFieldSet
from infrastructure.core.exception.business_error import BusinessError

from agile.base.api import NoAuthrizedApi
from agile.crm.manager.api import StaffAuthorizedApi
from abs.service.customer.manager import CustomerServer
