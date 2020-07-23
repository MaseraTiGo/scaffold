# coding=UTF-8

import random

from infrastructure.core.exception.business_error import BusinessError
from abs.common.manager import BaseManager
from abs.middleground.business.person.models import Person,\
        Address, BankCard, PersonStatus, PersonStatistics, Certification
from abs.middleware.extend.yunaccount import yunaccount_extend


class PersonServer(BaseManager):

    @classmethod
    def create(cls, **person_infos):
        person = Person.create(**person_infos)
        PersonStatus.create(person=person)
        PersonStatistics.create(person=person)
        return person

    @classmethod
    def get(cls, person_id):
        person = Person.get_byid(person_id)
        return person

    @classmethod
    def search(cls, current_page, **search_info):
        person_qs = Person.search(**search_info)
        return person_qs

    @classmethod
    def hung_persons(cls, obj_list):
        obj_mapping = {obj.person_id: obj for obj in obj_list}
        person_qs = Person.search(id__in=obj_mapping.keys())
        person_mapping = {person.id: person for person in person_qs}
        status_qs = PersonStatus.search(person_id__in=obj_mapping.keys())
        status_mapping = {status.person.id: status for status in status_qs}
        for obj in obj_list:
            obj.person = person_mapping.get(obj.person_id, None)
            obj.person_status = status_mapping.get(obj.person_id, None)
        return obj_list

    @classmethod
    def update(cls, person_id, **person_infos):
        person = cls.get(person_id)
        person.update(**person_infos)
        return person

    @classmethod
    def is_exsited(cls, phone):
        is_exsited, person = Person.is_exsited(phone)
        return is_exsited, person

    @classmethod
    def update_default_address(cls, person, address):
        status = PersonStatus.get_byperson(person)
        if status.default_address and status.default_address.id != address.id:
            status.update(default_address=address)
        return True

    @classmethod
    def add_address(cls, person_id, is_default, **address_info):
        person = cls.get(person_id)
        address = Address.create(
            person=person,
            **address_info
        )
        if is_default:
            cls.update_default_address(person, address)
        return address

    @classmethod
    def get_address(cls, address_id):
        address = Address.get_byid(address_id)
        status = PersonStatus.get_byperson(address.person)
        address.is_default = False
        if status and status.default_address:
            address.is_default = status.default_address.id == address.id
        return address

    @classmethod
    def get_all_address(cls, person_id):
        address_qs = Address.search(person=person_id)
        status = PersonStatus.get_byperson(person_id)
        address_list = []
        for address in address_qs:
            address.is_default = False
            if status.default_address:
                address.is_default = status.default_address.id == address.id
            address_list.append(address)
        return address_list

    @classmethod
    def remove_address(cls, address_id):
        return cls.get_address(address_id).delete()

    @classmethod
    def update_address(cls, address_id, is_default, **address_info):
        address = cls.get_address(address_id)
        address.update(**address_info)
        if is_default:
            cls.update_default_address(address.person, address)
        return address

    @classmethod
    def check_bankcard_valid(cls, name, identification, bank_number, phone):
        flag, result = yunaccount_extend.verify_bankcard_four_factor(
            name,
            identification,
            bank_number,
            phone
        )
        if not flag:
            raise BusinessError('银行卡四要素不匹配')

    @classmethod
    def check_bankcard_unique(cls, person_id, bank_number):
        if BankCard.is_exsited(person_id, bank_number):
            raise BusinessError('银行卡重复')

    @classmethod
    def add_bankcard(
        cls,
        person_id,
        bank_number,
        phone,
        identification,
        **bankcard_info
    ):
        person = cls.get(person_id)

        # todo: add card to verify
        bank_list = (
            ('中国工商银行', "ICBC"),
            ('中国邮政储蓄银行', "PSBC"),
            ('中国农业银行', "ABC"),
            ('中国银行', "BOC"),
            ('中国建设银行', "CCB"),
            ('中国交通银行', "COMM"),
            ('招商银行', "CMB"),
        )
        bank_name, bank_code = random.choice(bank_list)

        cls.check_bankcard_unique(person_id, bank_number)
        cls.check_bankcard_valid(
            bank_name,
            identification,
            bank_number,
            phone
        )
        bankcard = BankCard.create(
            person=person,
            bank_name=bank_name,
            bank_code=bank_code,
            bank_number=bank_number,
            **bankcard_info
        )
        return bankcard

    @classmethod
    def get_bankcard(cls, bankcard_id):
        bankcard = BankCard.get_byid(bankcard_id)
        return bankcard

    @classmethod
    def get_all_bankcard(cls, person_id):
        bankcard = BankCard.search(person=person_id)
        return bankcard

    @classmethod
    def remove_bankcard(cls, bankcard_id):
        return cls.get_bankcard(bankcard_id).delete()

    @classmethod
    def add_certification(cls, person_id, **certification_info):
        person = cls.get(person_id)
        status = PersonStatus.get_byperson(person)
        if status.certification:
            raise BusinessError('您已实名认证')
        certification = Certification.create(
            person=person,
            **certification_info
        )
        status.update(certification=certification)
        return certification

    @classmethod
    def get_person_certification(cls, person_id):
        person = cls.get(person_id)
        status = PersonStatus.get_byperson(person)
        if not status.certification:
            raise BusinessError('用户未实名认证')
        return status.certification

    @classmethod
    def get_person_status(cls, person_id):
        person = cls.get(person_id)
        return PersonStatus.get_byperson(person)
