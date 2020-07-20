# coding=UTF-8


from support.common.maker import BaseMaker
from support.common.generator.helper import AddressGenerator,\
        PersonGenerator, BankCardGenerator, StatusGenerator,\
        StatisticsGenerator
from support.environment.common.middleground.person.address import\
        AddressLoader
from support.environment.common.middleground.person.bankcard import\
        BankcardLoader


class PersonMaker(BaseMaker):
    """
    用户信息初始化
    """

    def __init__(self, person_info):
        self._person = PersonGenerator(person_info)
        self._address = AddressGenerator(AddressLoader().generate())
        self._bankcard = BankCardGenerator(BankcardLoader().generate())
        self._person_status = StatusGenerator()
        self._person_statistics = StatisticsGenerator()

    def generate_relate(self):
        self._person.add_outputs(
            self._address,
            self._bankcard,
            self._person_status,
            self._person_statistics
        )
        return self._person
