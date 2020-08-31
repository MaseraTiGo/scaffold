# coding=UTF-8

from infrastructure.log.base import logger
from infrastructure.utils.common.single import Single
from infrastructure.utils.common.dictwrapper import DictWrapper
from infrastructure.core.exception.api_error import ApiError
from infrastructure.core.exception.pro_error import ProtocolError, pro_errors, ProtocolCodes
from infrastructure.core.exception.business_error import BusinessError
from infrastructure.core.exception.debug_error import DebugError
from infrastructure.core.exception.system_error import SysError
from infrastructure.log.base import logger


class IService(object):

    _service_mapping = None

    def add(self, service, *services):
        if self._service_mapping is None:
            self._service_mapping = {}
        iter_list = [service]
        iter_list.extend(services)
        for cur_service in iter_list:
            self._service_mapping[cur_service.get_flag()] = cur_service
            cur_service.set_protocols(self)

    def get_service(self, flag):
        service = self._service_mapping.get(flag)
        if service:
            return service
        raise NotImplementedError('service is not exist')

    def get_services(self):
        return self._service_mapping.values()


class IChecker(object):

    @classmethod
    def get_check_funcs(cls):
        if not hasattr(cls, "_check_funcs"):
            cls._check_funcs = {key: function for key, function in cls.__dict__.items()\
                            if key.startswith("_check_")}
        return cls._check_funcs

    @classmethod
    def exec_check(cls, parms, all_parms):
        for check_func in cls.get_check_funcs().values():
            check_func(cls, parms, all_parms)


class BaseProtocol(Single, IService, IChecker):

    parser = None
    responser = None

    @classmethod
    def get_name(cls):
        raise NotImplementedError('Please imporlement this interface in subclass')

    @classmethod
    def get_desc(cls):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def parse(self, all_parms):
        data = all_parms.copy()
        pro_parms = {}
        fields = self.parser.get_fields()
        for field, helper in fields.items():
            if field in data:
                value = data.pop(field)
                try:
                    pro_parms[field] = helper.execute(value)
                except Exception as e:
                    raise pro_errors(ProtocolCodes.PROTOCOL_FORMAT_ERROR, field,
                                     helper.get_field().__class__.__name__)
            else:
                raise pro_errors(ProtocolCodes.PROTOCOL_LOST_PARAM, field)
        return DictWrapper(pro_parms), DictWrapper(data)

    def extract_parms(self, pro):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def get_service_flag(self, pro_parms):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def get_api_flag(self, pro_parms):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def get_success_parms(self, result):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def get_fail_parms(self, e):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def succeed(self, result):
        parms = self.get_success_parms(result)
        return self.responser.succeed(parms, result)

    def failed(self, e):
        parms = self.get_fail_parms(e)
        return self.responser.failed(parms)

    def run(self, pro):
        try:
            base_parms, data = self.extract_parms(pro)
            pro_parms, api_parms = self.parse(data)
            self.exec_check(pro_parms, data)
            service_str = self.get_service_flag(pro_parms)
            api_str = self.get_api_flag(pro_parms)
            api_parms.update(base_parms)
            result = self.get_service(service_str).run(api_str, api_parms)
            response = self.succeed(result)
            return response
        except DebugError as e:
            logger.exception(e)
            return self.failed(e)
        except ApiError as e:
            logger.exception(e)
            return self.failed(e)
        except ProtocolError as e:
            logger.exception(e)
            return self.failed(e)
        except BusinessError as e:
            # logger.exception(e)
            return self.failed(e)
        except Exception as e:
            logger.exception(e)
            system_error = SysError(e)
            return self.failed(system_error)
