# coding=UTF-8


from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.middleground.business.user.manager import UserServer
from abs.services.customer.personal.models import Customer


class CustomerServer(object):

    @classmethod
    def get(cls, customer_id):
        customer = Customer.get_byid(customer_id)
        UserServer.hung_users([customer])
        return customer

    @classmethod
    def search(cls, current_page, **search_info):
        customer_qs = Customer.search(**search_info)
        customer_qs.order_by('-create_time')
        splitor = Splitor(current_page, customer_qs)
        UserServer.hung_users(splitor.get_list())
        return splitor

    @classmethod
    def is_exsited(cls, phone):
        is_exsited, customer = Customer.is_exsited(phone)
        return is_exsited, customer

    @classmethod
    def create(cls, phone, **customer_info):
        is_user_exsited, user = UserServer.is_exsited(phone)
        if is_user_exsited:
            raise BusinessError('客户已存在，不能创建')

        user = UserServer.create(phone=phone, **customer_info)
        customer = Customer.create(
            user_id=user.id,
            phone=phone,
            **customer_info
        )
        return customer

    @classmethod
    def update(cls, customer_id, **update_info):
        customer = cls.get(customer_id)
        UserServer.update(customer.user_id, **update_info)
        customer.update(**update_info)
        return customer
