# coding=UTF-8


from abs.common.model import BaseModel, \
        CharField, DateTimeField, TextField, timezone


class PermissionBase(BaseModel):


    class Meta:
        abstract = True
