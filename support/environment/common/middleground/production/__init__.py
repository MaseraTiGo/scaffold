# coding=UTF-8


from support.common.maker import BaseMaker
# from support.common.generator.helper import BrandGenerator, \
#         ProductionGenerator
from support.common.generator.helper.middleground.production.brand import BrandGenerator
from support.common.generator.helper.middleground.production import ProductionGenerator
from support.environment.common.middleground.production.brand import\
        BrandLoader
from support.environment.common.middleground.production.production import\
        ProductionLoader


class ProductionMaker(BaseMaker):
    """
    用户信息初始化
    """

    def __init__(self):
        self._production = ProductionGenerator(
            ProductionLoader().generate()
        )
        self._brand = BrandGenerator(
            BrandLoader().generate()
        )

    def generate_relate(self):
        self._production.add_inputs(
            self._brand,
        )
        return self._production
