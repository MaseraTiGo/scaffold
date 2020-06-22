# coding=UTF-8

from infrastructure.utils.common.single import Single


class BaseAPIService(Single):

    _protocol_set = None
    _api_mapping = None

    @classmethod
    def get_name(cls):
        raise NotImplementedError('Please imporlement this interface in subclass')

    @classmethod
    def get_desc(cls):
        raise NotImplementedError('Please imporlement this interface in subclass')

    @classmethod
    def get_flag(cls):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def add(self, api, *apis):
        if self._api_mapping is None:
            self._api_mapping = {}
        iter_list = [api]
        iter_list.extend(apis)
        for cur_api in iter_list:
            self._api_mapping[cur_api.get_name()] = cur_api
            cur_api.set_service(self)

    def router(self, flag):
        api = self._api_mapping.get(flag, None)
        if api:
            return api
        raise NotImplementedError('api is not existed')

    def run(self, api_name, parms):
        api = self.router(api_name)
        return api().run(parms)

    def set_protocols(self, protocol, *protocols):
        if self._protocol_set is None:
            self._protocol_set = set([protocol])

        for _pro in protocols:
            self._protocol_set.add(_pro)

    def get_protocols(self):
        return list(self._protocol_set)

    def get_apis(self):
        return self._api_mapping.values()


class ToolAPIService(BaseAPIService):
    pass


class BusinessAPIService(BaseAPIService):
    pass


class RoleAPIService(BaseAPIService):
    pass
