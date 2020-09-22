# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.enterprise.manager import EnterpriseServer
from abs.middleground.business.person.manager import PersonServer
from abs.services.crm.staff.models import Staff


class StaffServer(BaseManager):

    STAFF_MODEL = Staff
