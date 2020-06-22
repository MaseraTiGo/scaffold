# coding=UTF-8

from infrastructure.core.field.adapter import AdapterField, AdapterFieldSet


class RequestField(AdapterField):

    def __init__(self, field_cls, is_need = True, *args, **kwargs):
        super(RequestField, self).__init__(field_cls, *args, **kwargs)

    def is_required(self):
        return self.get_field().is_required()

    def execute(self, value, *args, **kwargs):
        return self.get_field().parse(value, *args, **kwargs)


class RequestFieldSet(AdapterFieldSet):

    _field_cls = RequestField
