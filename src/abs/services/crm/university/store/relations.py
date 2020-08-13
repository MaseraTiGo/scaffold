# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone, \
        ForeignKey, CASCADE
from abs.services.crm.university.settings import DB_PREFIX
from abs.services.crm.university.store import School, Major



class Relations(BaseModel):
    school = ForeignKey(School, on_delete = CASCADE)
    major = ForeignKey(Major, on_delete = CASCADE)
    content = TextField(verbose_name = "描述", default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "relations"

    @classmethod
    def search(cls, **attrs):
        relations_qs = cls.query().filter(**attrs)
        return relations_qs
