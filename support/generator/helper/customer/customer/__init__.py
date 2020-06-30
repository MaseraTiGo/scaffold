# coding=UTF-8


from infrastructure.log.base import logger
from support.generator.base import BaseGenerator
from model.common.model_user_base import UserCertification
from model.store.model_customer import Customer


class CustomerGenerator(BaseGenerator):

    def __init__(self, customer_info):
        super(CustomerGenerator, self).__init__()
        self._customer_infos = self.init(customer_info)

    def get_create_list(self, result_mapping):
        return self._customer_infos

    def create(self, customer_info, result_mapping):
        user_certification_qs = UserCertification.query().filter(identification =
                                                                 customer_info.identification)
        if user_certification_qs.count():
            user_certification = user_certification_qs[0]
        else :
            user_certification = UserCertification.create(**customer_info)

        customer_qs = Customer.query().filter(phone = customer_info.phone)
        if customer_qs.count():
            customer = customer_qs[0]
        else:
            customer = Customer.create(certification = user_certification, **customer_info)
        return customer

    def delete(self):
        print('======================>>> delete customer <======================')
        return None
