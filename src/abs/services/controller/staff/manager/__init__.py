# coding=UTF-8


"""
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor
"""

from abs.middleground.business.person.assistor.staff.manager import\
        AbstractStaffServer
from abs.services.controller.staff.models import Staff


class StaffServer(AbstractStaffServer):

    STAFF_MODEL = Staff
