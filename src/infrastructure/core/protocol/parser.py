# coding=UTF-8

from infrastructure.core.field.adapter import AdapterField, AdapterFieldSet


class ParseField(AdapterField):

    def __init__(self, field_cls, *args, **kwargs):
        super(ParseField, self).__init__(field_cls, *args, **kwargs)

    def execute(self, value):
        return self.get_field().parse(value)


class Parser(object):

    def get_fields(self):
        if not hasattr(self, '_fields'):
            self._fields = {}
            for name, value in self.__dict__.items():
                if isinstance(value, ParseField):
                    self._fields[name] = value
        return self._fields

    @classmethod
    def get_field(self, name):
        fields = self.get_fields()
        return fields.get(name, None)
