# coding=UTF-8

from abs.middleground.business.enterprise.assistor.link.model import \
        AbstractCompany
from abs.services.crm.staff.settings import DB_PREFIX


class Company(AbstractCompany):

    class Meta:
        db_table = DB_PREFIX + "company"
