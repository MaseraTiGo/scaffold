# coding=UTF-8


class AdapterField(object):

    _field = None

    def __init__(self, field_cls, *args, **kwargs):
        self._field = field_cls(*args, **kwargs)

    def execute(self, value):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def get_field(self):
        return self._field

    def is_required(self):
        return self.get_field()._is_required

    def get_choices(self):
        return self.get_field()._choices

    def get_default(self):
        return self.get_field()._default

    def get_type(self):
        return self.get_field().get_type()

    def get_desc(self):
        return self.get_field().get_desc()


class AdapterFieldSet(object):

    _fields = None
    _field_cls = None

    def __init__(self):
        self._fields = self.get_fields()

    def __setattr__(self, name, value):
        _fields = super(AdapterFieldSet, self).__getattribute__('_fields')
        if name in _fields:
            value = _fields[name].execute(value)
        super(AdapterFieldSet, self).__setattr__(name, value)

    def __getattribute__(self, name):
        if not (name.startswith('__') and name.endswith('__')):
            attr_list = name.split("__")
            first_attr = attr_list[0]
            end_attr = attr_list[-1]

            _fields = super(AdapterFieldSet, self).__getattribute__('_fields')
            if _fields is not None and first_attr in _fields:
                if first_attr != end_attr:
                    helper = _fields[first_attr]
                    return getattr(helper.get_field(), end_attr)

        return super(AdapterFieldSet, self).__getattribute__(name)

    @classmethod
    def get_fields(cls):
        if cls._fields is None:
            cls._fields = {}
            for name in dir(cls):
                value = getattr(cls, name)
                if isinstance(value, cls._field_cls):
                    cls._fields[name] = value
        return cls._fields
