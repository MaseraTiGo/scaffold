# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import CustomerGenerator,\
        CustomerAccountGenerator
from support.environment.common.middleground.person import PersonMaker
from support.environment.simulate.business.customer.customer import \
        CustomerLoader


class CustomerSimulateMaker(BaseMaker):

    def generate_relate(self):
        customer_info = CustomerLoader().generate()
        customer = CustomerGenerator(customer_info)
        account = CustomerAccountGenerator()
        person = PersonMaker(customer_info).generate_relate()

        customer.add_outputs(
            account,
        )
        customer.add_inputs(
            person
        )
        return customer
