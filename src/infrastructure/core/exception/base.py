# coding=UTF-8

'''
Created on 2016-7-4

@author: YRK
'''

from infrastructure.utils.common.single import Single


class BaseError(Exception):

    code = None
    desc = None
    template = None

    def __init__(self, *args, **kwargs):
        assert self.code is not None
        assert self.desc is not None

        self.template = "{}" if self.template is None else self.template
        self.msg = self.generate_msg(*args, **kwargs)

    @classmethod
    def get_flag(cls):
        status = cls.__name__.lower().replace("error", "")
        return status

    @classmethod
    def get_code(cls):
        return cls.code

    @classmethod
    def get_desc(cls):
        return cls.desc

    @classmethod
    def get_template(cls):
        return cls.template

    def generate_msg(self, *args, **kwargs):
        return self.template.format(*args, **kwargs)

    def get_msg(self):
        return self.msg

    def __str__(self):
        return "[{code}] - {desc}".format(code=self.get_code(), desc=self.get_desc())

    def json(self):
        return {
            'msg': self.get_msg(),
            'code': self.get_code()
        }


class BaseErrorManager(Single):

    _error = None
    _valid_errors = None

    def __init__(self):
        assert self._valid_errors is not None
        assert type(self._valid_errors) is tuple
        assert len(self._valid_errors) > 0

        self._error = {} if self._error is None else self._error

    def regiter(self, error):
        assert issubclass(error, BaseError)

        if error.code in self._error:
            raise Exception("error {code} code have registed, error obj = {error}"\
                            .format(code=error.code, error=error))

        if error.code not in self._valid_errors:
            raise Exception("error {code} is invalied,  error obj = {error}"\
                            .format(code=error.code, error=error))

        self._error[error.code] = error

    def get_error(self, code):
        if code not in self._error:
            raise Exception("error {code} is invalied".format(code=code))
        return self._error[code]

    def get_errors(self):
        return list(self._error.values())

    def __call__(self, code, *args, **kwargs):
        return self.get_error(code)(*args, **kwargs)
