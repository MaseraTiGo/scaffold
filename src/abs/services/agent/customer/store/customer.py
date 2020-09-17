# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone
from abs.services.agent.customer.settings import DB_PREFIX
from abs.services.agent.customer.utils.constant import SourceTypes, \
     EducationTypes
from abs.middleground.business.person.utils.constant import GenderTypes


class AgentCustomer(BaseModel):

    agent_id = IntegerField(verbose_name = "agent_id")
    person_id = IntegerField(verbose_name = "person_id", default = 0)
    name = CharField(verbose_name = "客户姓名", max_length = 16, default = '')
    phone = CharField(verbose_name = "手机号码", max_length = 16, default = '')
    city = CharField(verbose_name = "地址", max_length = 128, default = '')
    education = CharField(verbose_name = "学历", max_length = 32, \
                          choices = EducationTypes.CHOICES, \
                          default = EducationTypes.OTHER)
    gender = CharField(
        verbose_name = "性别",
        max_length = 24,
        choices = GenderTypes.CHOICES,
        default = GenderTypes.UNKNOWN
    )
    source = CharField(verbose_name = "客户来源", max_length = 64, default = '')
    wechat = CharField(verbose_name = "客户微信", max_length = 64, default = '')
    qq = CharField(verbose_name = "客户qq", max_length = 32, default = '')
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "base"

    @classmethod
    def search(cls, **attrs):
        agent_customer_qs = cls.query().filter(**attrs)
        return agent_customer_qs
