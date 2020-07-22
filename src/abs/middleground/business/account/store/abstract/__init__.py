# coding=UTF-8


from abs.common.model import BaseModel,\
        IntegerField, CharField, DateTimeField, timezone
from abs.middleground.business.account.utils.constant import StatusTypes,\
        PlatformTypes


class BaseAccount(BaseModel):
    """
    全平台账号使用的基类
    """
    username = CharField(verbose_name="账号", max_length=64)
    password = CharField(verbose_name="密码", max_length=64)
    last_login_time = DateTimeField(verbose_name="最后一次登录时间", null=True)
    last_login_ip = CharField(verbose_name="最后登录ip", max_length=64, default='')
    register_ip = CharField(verbose_name="注册IP", max_length=64, default='')
    status = CharField(
        verbose_name="账号状态",
        max_length=64,
        choices=StatusTypes.CHOICES,
        default=StatusTypes.NOTACTIVE
    )
    role_type = CharField(
        verbose_name="角色",
        choices=PlatformTypes.CHOICES,
        max_length=24
    )
    role_id = IntegerField(verbose_name="角色id")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        abstract = True
        unique_together = (
            ('role_type', 'role_id'),
        )

    @classmethod
    def create(cls, **account_info):
        account_info.update({
            'role_type': cls.get_role_type()
        })
        return super(BaseAccount, cls).create(
            **account_info
        )

    def update(self, **account_info):
        account_info.update({
            'role_type': self.get_role_type()
        })
        return super(BaseAccount, self).update(
            **account_info
        )

    @classmethod
    def query(cls, **search_info):
        return super(BaseAccount, cls).query().filter(
            role_type=cls.get_role_type()
        )

    @classmethod
    def get_role_type(cls):
        return NotImplemented(
            "this interface is need to implemented!"
        )

    @classmethod
    def search(cls, **attrs):
        account_qs = cls.query().filter(
            **attrs
        )
        return account_qs

    @classmethod
    def is_exsited(cls, username, password):
        account_qs = cls.search(
            username=username,
            password=password
        )
        if account_qs.count():
            return True, account_qs[0]
        return False, None

    @classmethod
    def get_byusername(cls, username):
        try:
            return cls.search(
                username=username
            )[0]
        except Exception as e:
            return None

    @classmethod
    def get_byrole(cls, role_id):
        try:
            return cls.search(
                role_id=role_id
            )[0]
        except Exception as e:
            return None
