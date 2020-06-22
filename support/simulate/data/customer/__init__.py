# coding=UTF-8

from support.generator.helper import *
from support.simulate.data.base import BaseMaker
from support.simulate.tool.template.customer import *


class CustomerMaker(BaseMaker):

    def generate_relate_bycustomer(self):
        return staff_generator

    def generate_relate_bystaff(self,\
            customer_generator, chance_generator,\
                order_generator, order_item_generator,\
                    logistics_generator, logistics_item_generator,\
                        service_generator, service_item_generator):
        customer_generator.add_outputs(chance_generator)
        chance_generator.add_outputs(order_generator)
        order_generator.add_outputs(order_item_generator)
        order_item_generator.add_outputs(logistics_generator)
        logistics_generator.add_outputs(logistics_item_generator)
        logistics_item_generator.add_outputs(service_generator)
        service_generator.add_outputs(service_item_generator)
        return customer_generator

    def generate(self):
        customer_template = CustomerTemplate().generate()
        customer_generator = CustomerGenerator(customer_template)

        chance_template = SaleChanceTemplate().generate()
        chance_generator = SaleChanceGenerator(chance_template)

        order_template = OrderTemplate().generate()
        order_generator = OrderGenerator(order_template)

        order_item_template = OrderItemTemplate().generate()
        order_item_generator = OrderItemGenerator(order_item_template)

        logistics_generator = LogisticsGenerator()
        logistics_item_generator = LogisticsItemGenerator()

        service_generator = ServiceGenerator()
        service_item_generator = ServiceItemGenerator()

        customer_generator = self.generate_relate_bystaff(
            customer_generator,
            chance_generator,
            order_generator,
            order_item_generator,
            logistics_generator,
            logistics_item_generator,
            service_generator,
            service_item_generator,
        )
        customer_generator.generate()
        return customer_generator
