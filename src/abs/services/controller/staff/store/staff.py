# coding=UTF-8

from abs.common.model import CASCADE, ForeignKey
from abs.middleground.business.person.assistor.staff.model import \
        AbstractStaff
from abs.services.controller.staff.settings import DB_PREFIX
from abs.services.controller.staff.store.company import Company


class Staff(AbstractStaff):
    company = ForeignKey(Company, on_delete=CASCADE)

    class Meta:
        db_table = DB_PREFIX + "base"
