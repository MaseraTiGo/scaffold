# coding=UTF-8


from support.common.maker import BaseMaker
from support.common.generator.helper import SchoolGenerator, \
         MajorGenerator, RelationsGenerator, YearsGenerator


class YearsMaker(BaseMaker):
    """
    学校专业学年信息初始化
    """

    def __init__(self, school_info, major_info, years_info):
        self._school = SchoolGenerator(
            school_info
        )
        self._major = MajorGenerator(
            major_info
        )
        self._years = YearsGenerator(
            years_info
        )
        self._relations = RelationsGenerator()


    def generate_relate(self):
        self._relations.add_inputs(
            self._school, self._major
        )
        self._years.add_inputs(
            self._relations
        )
        return self._years
