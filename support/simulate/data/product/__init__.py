# coding=UTF-8

from support.simulate.data.base import BaseMaker
from support.generator.helper import *
from support.init.loader import *
from support.simulate.tool.template.product import ProductTemplate, ProductModelTemplate,\
        ChannelTemplate, ShopTemplate, GoodsTemplate


class ProductMaker(BaseMaker):

    def generate_relate(self, product_generator, product_model_generator,
                        channel_generator, shop_generator, goods_generator):

        product_model_generator.add_inputs(product_generator)
        shop_generator.add_inputs(channel_generator)
        goods_generator.add_inputs(product_model_generator, shop_generator)
        return goods_generator

    def generate(self):
        product_template = ProductTemplate().generate()

        product_generator = ProductGenerator(product_template)
        product_name = product_template['name']
        product_model_template = ProductModelTemplate(product_name).generate()

        product_model_generator = ProductModelGenerator(product_model_template)

        channel_template = ChannelTemplate().generate()
        channel_generator = ChannelGenerator(channel_template)
        shop_template = ShopTemplate(channel_template['name']).generate()
        shop_generator = ShopGenerator(shop_template)

        goods_template = GoodsTemplate(product_name, shop_template['name']).generate()
        goods_generator = GoodsGenerator(goods_template)

        goods_generator = self.generate_relate(product_generator, product_model_generator, \
                                channel_generator, shop_generator, goods_generator)
        goods_generator.generate()
        return goods_generator
