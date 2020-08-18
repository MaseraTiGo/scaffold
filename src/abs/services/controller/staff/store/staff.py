# coding=UTF-8

from abs.middleground.business.person.assistor.staff.model import \
        AbstractStaff
from abs.services.controller.staff.settings import DB_PREFIX


class Staff(AbstractStaff):

    class Meta:
        db_table = DB_PREFIX + "base"
