# coding=UTF-8

import random

from support.common.generator.base import BaseGenerator
from abs.services.crm.adsense.models import Space


class SpaceGenerator(BaseGenerator):

    def __init__(self, space_info):
        super(SpaceGenerator, self).__init__()
        self._space_infos = self.init(space_info)

    def get_create_list(self, result_mapping):
        return self._space_infos

    def create(self, space_info, result_mapping):
        space_qs = Space.query().filter(label = space_info.label)
        if space_qs.count():
            space = space_qs[0]
        else:
            space = Space.create(
                        **space_info
                    )
        return space

    def delete(self):
        print('======================>>> delete space <======================')
        return None
