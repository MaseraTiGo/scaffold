# coding=UTF-8

from infrastructure.core.field.adapter import AdapterField, AdapterFieldSet


class ResponseField(AdapterField):

    def __init__(self, field_cls, *args, **kwargs):
        super(ResponseField, self).__init__(field_cls, *args, **kwargs)

    def execute(self, value, is_safe):
        helper = self.get_field()
        value =  helper.format(value)
        if is_safe:
            return helper.reprocess(value)
        else:
            return value


class ResponseFieldSet(AdapterFieldSet):
    _field_cls = ResponseField

    def __init__(self):
        self._fields = self.get_fields()
        self._is_safe = False

    def on_safe(self):
        self._is_safe = True

    def off_safe(self):
        self._is_safe = False

    def __setattr__(self, name, value):
        _fields = super(AdapterFieldSet, self).__getattribute__('_fields')
        if name in _fields:
            value = _fields[name].execute(value, self._is_safe)
        super(AdapterFieldSet, self).__setattr__(name, value)
