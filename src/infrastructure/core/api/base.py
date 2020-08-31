# coding=UTF-8

from infrastructure.core.api.request import RequestFieldSet
from infrastructure.core.api.response import ResponseFieldSet, ResponseField
from infrastructure.core.exception.api_error import ApiCodes, api_errors


class ApiInterface(object):

    @classmethod
    def get_name(cls, level=3):
        name = cls.__name__.lower()
        namespace = '.'.join(cls.__module__.split('.')[level:])
        return '.'.join([namespace, name])

    @classmethod
    def is_auth(cls):
        return True

    @classmethod
    def get_desc(cls):
        return cls.__doc__.strip()

    @classmethod
    def get_author(cls):
        return "yrk"

    @classmethod
    def get_version(cls):
        return "v1.0"

    @classmethod
    def get_discard(cls):
        """ set discard time """
        return None


class ApiHelper(object):

    _service = None

    @classmethod
    def set_service(cls, service):
        cls._service = service

    @classmethod
    def get_service(cls):
        return cls._service


class BaseApi(ApiInterface, ApiHelper):

    request = None
    response = None

    def __init__(self):
        assert self.request is not None
        assert issubclass(self.request, RequestFieldSet)

        assert self.response is not None
        assert issubclass(self.response, ResponseFieldSet)

        self.request = type(
            'tmp' + self.request.__name__,
            (self.request,),
            {}
        )()
        self.response = type(
            'tmp' + self.response.__name__,
            (self.response,),
            {}
        )()

    def parse(self, request, parms):
        for key, helper in request.get_fields().items():
            if key not in parms and helper.get_field().is_required():
                raise api_errors(ApiCodes.INTERFACE_PARATERS_LOST, key)
            else:
                try:
                    setattr(request, key, parms[key])
                except Exception as e:
                    raise api_errors(
                        ApiCodes.INTERFACE_PARATERS_PARSE_WRONG,
                        key,
                        e
                    )
        return request

    def authorized(self, request, parms):
        raise NotImplementedError(
            'Please imporlement this interface in subclass'
        )

    def execute(self, *args, **kwargs):
        raise NotImplementedError(
            'Please imporlement this interface in subclass'
        )

    def fill(self, response, *args):
        raise NotImplementedError(
            'Please imporlement this interface in subclass'
        )

    def pack(self, response, result):
        if result is None:
            return None

        args = result if type(result) is tuple else [result]

        if args:
            response = self.fill(response, *args)

        pack_data = {}
        for key in response.get_fields():
            value = getattr(response, key)
            if isinstance(value, ResponseField):
                raise Exception("response lose paramter {}".format(key))
            pack_data[key] = value

        return pack_data

    def record(self, api_parms):
        print('record api ....')
        return True

    def run(self, parms):
        request = self.parse(self.request, parms)
        self.authorized(request, parms)
        result = self.execute(request)
        response_data = self.pack(self.response, result)
        return response_data

    @classmethod
    def get_request_fields(cls):
        """get request fields"""
        if cls.request is None:
            print("request is empty!!!")
            return {}
        return cls.request.get_fields()

    @classmethod
    def get_response_fields(cls):
        """get response fields"""
        if cls.response is None:
            print("response is empty!!!")
            return {}
        return cls.response.get_fields()
