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
        customer = cls.get_byid(customer_id)
        UserServer.update(customer.user_id, **update_info)
        customer.update(**update_info)
        return customer

    """

    @classmethod
    def add_address(cls, customer_id, **address_info):
        customer = cls.get_byid(customer_id)
        address = CustomerAddress.create(customer = customer, **address_info)
        return address

    @classmethod
    def get_address(cls, address_id):
        address = CustomerAddress.get_byid(address_id)
        return address

    @classmethod
    def get_all_address(cls, customer_id):
        address_qs = CustomerAddress.search(customer = customer_id)
        return address_qs

    @classmethod
    def remove_address(cls, address_id):
        return cls.get_address(address_id).delete()

    @classmethod
    def update_address(cls, address_id, **address_info):
        address = cls.get_address(address_id)
        address.update(**address_info)
        return address

    @classmethod
    def add_bankcard(cls, customer_id, bank_number, **bankcard_info):
        customer = cls.get_byid(customer_id)

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

        bankcard = CustomerBankCard.create(customer = customer, bank_name = bank_name, bank_code =
                                           bank_code, bank_number = bank_number, **bankcard_info)
        return bankcard

    @classmethod
    def get_bankcard(cls, bankcard_id):
        bankcard = CustomerBankCard.get_byid(bankcard_id)
        return bankcard

    @classmethod
    def get_all_bankcard(cls, customer_id):
        bankcard = CustomerBankCard.search(customer = customer_id)
        return bankcard

    @classmethod
    def remove_bankcard(cls, bankcard_id):
        return cls.get_bankcard(bankcard_id).delete()
    """
