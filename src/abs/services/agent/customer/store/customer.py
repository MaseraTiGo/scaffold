# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.agent.customer.settings import DB_PREFIX
from abs.services.agent.customer.utils.constant import SourceTypes, \
     EducationTypes


class AgentCustomer(BaseModel):

    agent_id = IntegerField(verbose_name = "agent_id")
    customer_id = IntegerField(verbose_name = "customer_id", default = 0)
    person_id = IntegerField(verbose_name = "person_id", default = 0)
    name = CharField(verbose_name = "客户姓名", max_length = 16, default = '')
    phone = CharField(verbose_name = "手机号码", max_length = 16, default = '')
    city = CharField(verbose_name = "地址", max_length = 128, default = '')
    education = CharField(verbose_name = "学历", max_length = 32, \
                          choices = EducationTypes.CHOICES, \
                          default = EducationTypes.OTHER)
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        agent_customer_qs = cls.query().filter(**attrs)
        return agent_customer_qs
