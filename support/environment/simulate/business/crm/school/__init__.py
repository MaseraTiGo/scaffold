# coding=UTF-8
import random

from support.common.generator.field.normal import \
        SchoolHelper
from support.common.maker import BaseLoader


class CrmSchoolLoader(BaseLoader):

    def generate(self):
        times = random.randint(3, 10)
        school_list = []
        for _ in range(times):
            name, content, province, city = SchoolHelper().generate()
            school = {
                'name': name,
                'content': content,
                'province':province,
                'city': city,
            }
            school_list.append(school)
        return school_list
