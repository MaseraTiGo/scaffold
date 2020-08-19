# coding=UTF-8
import random

from support.common.generator.field.model import \
        DurationTypesConstant, CategoryTypesConstant
from support.common.maker import BaseLoader


class CrmYearsLoader(BaseLoader):

    def generate(self):
        times = random.randint(3, 10)
        years_list = []
        for _ in range(times):
            years = {
                'category': CategoryTypesConstant().generate(),
                'duration':DurationTypesConstant().generate(),
            }
            years_list.append(years)
        return years_list
