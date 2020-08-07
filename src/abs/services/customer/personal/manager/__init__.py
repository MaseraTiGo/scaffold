# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.middleground.business.person.manager import PersonServer
from abs.services.customer.personal.models import Customer


class CustomerServer(BaseManager):

    @classmethod
    def get(cls, customer_id):
        customer = Customer.get_byid(customer_id)
        PersonServer.hung_persons([customer])
        return customer

    @classmethod
    def search(cls, current_page, **search_info):
        customer_qs = Customer.search(**search_info).order_by('-create_time')
        splitor = Splitor(current_page, customer_qs)
        PersonServer.hung_persons(splitor.get_list())
        return splitor

    @classmethod
    def is_exsited(cls, phone):
        is_exsited, person = PersonServer.is_exsited(phone)
        return is_exsited, person

    @classmethod
    def create(cls, phone, **customer_info):
        is_person_exsited, person = PersonServer.is_exsited(phone)
        if is_person_exsited:
            raise BusinessError('客户已存在，不能创建')

        person = PersonServer.create(phone = phone, **customer_info)
        customer = Customer.create(
            person_id = person.id,
            phone = phone,
            **customer_info
        )
        return customer

    @classmethod
    def update(cls, customer_id, **update_info):
        customer = cls.get(customer_id)
        PersonServer.update(customer.person_id, **update_info)
        customer.update(**update_info)
        return customer

    @classmethod
    def get_customer_bankcard(cls, customer_id):
        customer = Customer.get_byid(customer_id)
        bankcard_list = PersonServer.get_all_bankcard(customer.person_id)
        return bankcard_list

    @classmethod
    def get_customer_address(cls, customer_id):
        customer = Customer.get_byid(customer_id)
        address_list = PersonServer.get_all_address(customer.person_id)
        return address_list

    @classmethod
    def hung_customer(cls, obj_list):
        customer_mapping = {}
        for obj in obj_list:
            obj.customer = None
            if obj.customer_id not in customer_mapping:
                customer_mapping[obj.customer_id] = []
            customer_mapping[obj.customer_id].append(obj)
        customer_list = list(Customer.search(id__in = customer_mapping.keys()))
        PersonServer.hung_persons(customer_list)
        for customer in customer_list:
            if customer.id in customer_mapping:
                for obj in customer_mapping[customer.id]:
                    obj.customer = customer
        return obj_list
