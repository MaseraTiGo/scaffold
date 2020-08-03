# coding=UTF-8


from support.common.maker import BaseMaker
from support.common.generator.helper import MerchandiseGenerator, \
     SpecificationGenerator


class MerchandiseMaker(BaseMaker):
    """
    商品信息初始化
    """

    def __init__(self, merchandise_info):
        self._merchandise = MerchandiseGenerator(merchandise_info)
        self._specification = SpecificationGenerator()

    def generate_relate(self):
        self._merchandise.add_outputs(
            self._specification,
        )
        return self._merchandise
