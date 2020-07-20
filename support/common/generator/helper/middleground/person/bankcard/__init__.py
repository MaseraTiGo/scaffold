# coding=UTF-8


from infrastructure.log.base import logger
from support.common.generator.base import BaseGenerator
from support.common.generator.helper import PersonGenerator
from abs.middleground.business.person.store import BankCard


class BankCardGenerator(BaseGenerator):

    def __init__(self, bankcard_infos):
        super(BankCardGenerator, self).__init__()
        self._bankcard_infos = self.init(bankcard_infos)

    def get_create_list(self, result_mapping):
        person_list = result_mapping.get(PersonGenerator.get_key())
        bankcard_list = []
        for person in person_list:
            for bankcard_info in self._bankcard_infos:
                bankcard_info.update({
                    'person': person
                })
                bankcard_list.append(bankcard_info)
        return bankcard_list

    def create(self, person_info, result_mapping):
        bankcard = BankCard.create(**person_info)
        return bankcard

    def delete(self):
        logger.info('================>>> delete person <==================')
        return None
