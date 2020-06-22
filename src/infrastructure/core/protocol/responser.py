# coding=UTF-8

from infrastructure.core.field.adapter import AdapterField


class ResponseField(AdapterField):

    def __init__(self, field_cls, is_success = True, is_error = True, *args, **kwargs):
        super(ResponseField, self).__init__(field_cls, *args, **kwargs)
        self._is_success = is_success
        self._is_error = is_error

    def is_success(self):
        return self._is_success

    def is_error(self):
        return self._is_error

    def execute(self, value):
        return self.get_field().format(value)


class Responser(object):

    RESULT_FLAG = "result"

    def get_success_fields(self):
        if not hasattr(self, "_success_fields"):
            self._success_fields = {}
            for name, value in self.__dict__.items():
                if isinstance(value, ResponseField) and value.is_success():
                    self._success_fields[name] = value
        return self._success_fields

    def get_fail_fields(self):
        if not hasattr(self, "_fail_fields"):
            self._fail_fields = {}
            for name, value in self.__dict__.items():
                if isinstance(value, ResponseField) and value.is_error():
                    self._fail_fields[name] = value
        return self._fail_fields

    def _pack(self, fields, pro_parm):
        response = {}
        for key, helper in fields.items():
            if key not in pro_parm:
                raise Exception("protocol response losted key {}".format(key))
            response[key] = helper.execute(pro_parm[key])
        return response

    def succeed(self, pro_parm, result, **kwargs):
        fields = self.get_success_fields()
        pro_parm.update(kwargs)
        response = self._pack(fields, pro_parm)
        response.update({self.RESULT_FLAG: result})
        return response

    def failed(self, pro_parm, **kwargs):
        fields = self.get_fail_fields()
        pro_parm.update(kwargs)
        response = self._pack(fields, pro_parm)
        return response
