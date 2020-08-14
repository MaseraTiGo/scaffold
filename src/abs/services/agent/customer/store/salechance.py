# coding=UTF-8

from abs.common.model import BaseModel, BooleanField, \
        IntegerField, CharField, TextField, DateTimeField, timezone, \
        DateField, ForeignKey, CASCADE
from abs.services.agent.customer.settings import DB_PREFIX
from abs.services.agent.customer.utils.constant import SourceTypes, \
     EducationTypes
from abs.services.agent.customer.store import AgentCustomer


class AgentCustomerSaleChance(BaseModel):
    agent_customer = ForeignKey(AgentCustomer, on_delete = CASCADE)
    staff_id = IntegerField(verbose_name = "所属机会员工id")
    founder_id = IntegerField(verbose_name = "创建机会员工id")
    organization_id = IntegerField(verbose_name = "组织id")
    product_id = IntegerField(verbose_name = "产品id")
    education = CharField(verbose_name = "学历", max_length = 32, \
                          choices = EducationTypes.CHOICES, \
                          default = EducationTypes.OTHER)
    city = CharField(verbose_name = "地址", max_length = 128, default = '')
    end_time = DateField(verbose_name = "机会截至时间", \
                         max_length = 20, null = False, \
                         blank = False)
    batch_no = CharField(verbose_name = "批号", max_length = 128, default = '')
    source = CharField(verbose_name = "来源", max_length = 64, \
                       choices = SourceTypes.CHOICES, \
                       default = SourceTypes.CREATE)
    is_end = BooleanField(verbose_name = "机会是否手动结束", default = False)
    remark = TextField(verbose_name = "备注", default = "")
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "salechance"

    @classmethod
    def search(cls, **attrs):
        sale_chance_qs = cls.query().filter(**attrs)
        return sale_chance_qs


class SaleChanceOrder(BaseModel):
    """机会订单关系表"""
    sale_chance = ForeignKey(AgentCustomerSaleChance, on_delete = CASCADE)
    order_id = IntegerField(verbose_name = "订单id")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        sale_chance_order_qs = cls.query().filter(**attrs)
        return sale_chance_order_qs