# coding=UTF-8

from support.generator.helper import *
from support.simulate.data.base import BaseMaker
from support.simulate.tool.template.customer import *


class CustomerMaker(BaseMaker):

    def generate_relate(self, \
                customer_generator, account_generator):
        customer_generator.add_outputs(account_generator)
        return customer_generator


    def generate(self):
        customer = CustomerGenerator(CustomerTemplate().generate())
        account = CustomerAccountGenerator()

        customer_generator = self.generate_relate(
            customer,
            account
        )
        customer_generator.generate()
        return customer_generator

