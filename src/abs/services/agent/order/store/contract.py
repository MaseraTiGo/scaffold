# coding=UTF-8

from abs.common.model import BaseModel, timezone, \
        IntegerField, CharField, TextField, DateTimeField
from abs.services.agent.order.settings import DB_PREFIX
from abs.services.agent.order.utils.constant import ContractStatus


class Contract(BaseModel):
    number = CharField(verbose_name = "合同编号", max_length = 64, default = '')
    agent_customer_id = IntegerField(verbose_name = "客户id", default = 0)
    agent_id = IntegerField(verbose_name = "代理商id")
    person_id = IntegerField(verbose_name = "用户id", default = 0)
    company_id = IntegerField(verbose_name = "公司id", default = 0)
    order_item_id = IntegerField(verbose_name = "订单商品详情id", default = 0)
    order_id = IntegerField(verbose_name = "订单id", default = 0)
    template_id = IntegerField(verbose_name = "合同模板id", default = 0)
    name = CharField(verbose_name = "名称", max_length = 32)
    phone = CharField(verbose_name = "联系电话", max_length = 16, default = "")
    email = CharField(verbose_name = "emali", max_length = 128, default = "")
    identification = CharField(verbose_name = "身份证号", max_length = 24, default = "")
    autograph = TextField(verbose_name = "签名URL", default = "")
    url = TextField(verbose_name = "合同url", default = "[]")
    img_url = TextField(verbose_name = "合同图片", default = '[]')
    status = CharField(
        verbose_name = "合同状态",
        max_length = 64,
        choices = ContractStatus.CHOICES,
        default = ContractStatus.WAIT_SEND
    )
    send_email_number = IntegerField(verbose_name = "发送邮件次数", default = 0)
    content = TextField(verbose_name = "合同参数", default = '[]')

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    class Meta:
        db_table = DB_PREFIX + "contract"

    @classmethod
    def search(cls, **attrs):
        contract_qs = cls.query().filter(**attrs)
        return contract_qs
