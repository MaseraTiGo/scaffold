# coding=UTF-8


from infrastructure.log.base import logger
from infrastructure.utils.common.dictwrapper import DictWrapper
from support.common.generator.base import BaseGenerator

from abs.services.crm.contract.models import Param


class ParamGenerator(BaseGenerator):

    def __init__(self, param_infos):
        super(ParamGenerator, self).__init__()
        self._param_infos = self.init(param_infos)

    def get_create_list(self, result_mapping):
        return self._param_infos

    def create(self, param_info, result_mapping):
        param_qs = Param.query(
            name_key = param_info.name_key,
        )
        if param_qs.count():
            param = param_qs[0]
        else:
            param = Param.create(**param_info)
        return param

    def delete(self):
        logger.info('================> delete param <==================')
        return None
