# coding=UTF-8

from support.common.maker import BaseMaker
from support.generator.helper import *
from support.simulate.tool.template.customer import *
from support.simulate.tool.template.customer_address import *
from support.simulate.tool.template.customer_bankcard import *
from support.simulate.tool.template.customer_finance import *


class CustomerMaker(BaseMaker):

    def generate_relate(
        self,
        customer_generator,
        account_generator,
        address_generator,
        bankcard_generator,
        balance_generator
    ):
        customer_generator.add_outputs(
            account_generator,
            address_generator,
            bankcard_generator,
            balance_generator
        )
        return customer_generator

    def generate(self):
        customer = CustomerGenerator(CustomerTemplate().generate())
        account = CustomerAccountGenerator()
        address = CustomerAddressGenerator(CustomerAddressTemplate().generate())
        bankcard = CustomerBankcardGenerator(CustomerBankcardTemplate().generate())
        balance = CustomerBalanceGenerator(CustomerBalanceTemplate().generate())

        customer_generator = self.generate_relate(
            customer,
            account,
            address,
            bankcard,
            balance,
        )
        customer_generator.generate()
        return customer_generator
