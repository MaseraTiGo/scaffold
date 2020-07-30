# coding=UTF-8
import random

from support.common.generator.field.normal import \
        MajorHelper
from support.common.maker import BaseLoader


class CrmMajorLoader(BaseLoader):

    def generate(self):
        times = random.randint(3, 10)
        major_list = []
        for _ in range(times):
            name, content, = MajorHelper().generate()
            major = {
                'name': name,
                'content': content,
            }
            major_list.append(major)
        return major_list
