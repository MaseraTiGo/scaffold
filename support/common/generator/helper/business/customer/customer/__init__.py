# coding=UTF-8


from support.common.generator.base import BaseGenerator
from abs.middleground.business.person.models import Person,\
        PersonStatus, PersonStatistics
from abs.services.customer.personal.models import Customer


class CustomerGenerator(BaseGenerator):

    def __init__(self, customer_info):
        super(CustomerGenerator, self).__init__()
        self._customer_infos = self.init(customer_info)

    def get_create_list(self, result_mapping):
        return self._customer_infos

    def create(self, customer_info, result_mapping):
        is_exsitd, person = Person.is_exsited(customer_info.phone)
        if not is_exsitd:
            person = Person.create(**customer_info)
            PersonStatus.create(person=person)
            PersonStatistics.create(person=person)

        customer_qs = Customer.search(person_id=person.id)
        if customer_qs.count() > 0:
            return customer_qs[0]
        else:
            customer = Customer.create(
                person_id=person.id,
                **customer_info
            )
            return customer

    def delete(self):
        print('===================>>> delete customer <====================')
        return None
