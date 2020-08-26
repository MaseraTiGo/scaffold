# coding=UTF-8

from abs.services.customer.account.settings import DB_PREFIX
from abs.common.model import BaseModel, ForeignKey, CASCADE, \
    IntegerField, CharField, DateTimeField, timezone
from abs.services.customer.account.store.account import CustomerAccount


class Tripartite(BaseModel):
    """
    第三方账号表
    """
    customer_account = ForeignKey(CustomerAccount, on_delete=CASCADE)
    category = CharField(verbose_name="分类", max_length=64)
    openid = CharField(verbose_name="openid", max_length=128, default='')

    class Meta:
        db_table = DB_PREFIX + "tripartite"

