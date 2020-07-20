# coding=UTF-8

from support.common.maker import BaseMaker
from support.common.generator.helper import CustomerGenerator,\
        CustomerAccountGenerator
from support.environment.init.business.customer.customer import CustomerLoader


class CustomerInitializeMaker(BaseMaker):
    """
    仅仅管理客户端初始化的数据(测试账号)
    1、测试用户及测试账号初始化
    2、客户商品数据
    """

    def __init__(self):
        self._customer = CustomerGenerator(CustomerLoader().generate())
        self._customer_account = CustomerAccountGenerator()

    def generate_relate(self):
        self._customer.add_outputs(self._customer_account)
        return self._customer


if __name__ == "__main__":
    CustomerInitializeMaker().run()
