# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import CustomerGenerator,\
        CustomerAccountGenerator, CustomerBalanceGenerator,\
        EnterpriseGenerator
from support.environment.common.middleground.person import PersonMaker
from support.environment.init.business.crm.enterprise import EnterpriseLoader
from support.environment.simulate.business.customer.customer import \
        CustomerLoader
from support.environment.simulate.business.customer.finance import \
        CustomerBalanceLoader


class CustomerSimulateMaker(BaseMaker):

    def generate_relate(self):
        customer_info = CustomerLoader().generate()
        enterprise = EnterpriseGenerator(EnterpriseLoader().generate())
        customer = CustomerGenerator(customer_info)
        account = CustomerAccountGenerator()
        person = PersonMaker(customer_info).generate_relate()
        balance = CustomerBalanceGenerator(
            CustomerBalanceLoader().generate()
        )

        customer.add_outputs(
            account,
            balance
        )
        customer.add_inputs(
            person,
            enterprise
        )
        return customer
