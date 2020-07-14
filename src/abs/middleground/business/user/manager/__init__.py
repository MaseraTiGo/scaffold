# coding=UTF-8

from abs.middleground.business.user.models import User,\
        Address, UserStatus


class UserServer(object):

    @classmethod
    def create(cls, **user_infos):
        user = User.create(**user_infos)
        UserStatus.create(user=user)
        return user

    @classmethod
    def get(cls, user_id):
        user = User.get_byid(user_id)
        return user

    @classmethod
    def search(cls, current_page, **search_info):
        user_qs = User.search(**search_info)
        return user_qs

    @classmethod
    def hung_users(cls, obj_list):
        obj_mapping = {obj.user_id: obj for obj in obj_list}
        user_qs = User.search(id__in=obj_mapping.keys())
        user_mapping = {user.id: user for user in user_qs}
        status_qs = UserStatus.search(user_id__in=obj_mapping.keys())
        status_mapping = {status.user.id: status for status in status_qs}
        for obj in obj_list:
            obj.user = user_mapping.get(obj.user_id, None)
            obj.user_status = status_mapping.get(obj.user_id, None)
        return obj_list

    @classmethod
    def update(cls, user_id, **user_infos):
        user = cls.get(user_id)
        user.update(**user_infos)
        return user

    @classmethod
    def is_exsited(cls, phone):
        is_exsited, user = User.is_exsited(phone)
        return is_exsited, user

    @classmethod
    def update_default_address(cls, user, address):
        status = UserStatus.get_byuser(user)
        if status.default_address and status.default_address.id != address.id:
            status.update(default_address=address)
        return True

    @classmethod
    def add_address(cls, user_id, is_default, **address_info):
        user = cls.get(user_id)
        address = Address.create(
            user=user,
            **address_info
        )
        if is_default:
            cls.update_default_address(user, address)
        return address

    @classmethod
    def get_address(cls, address_id):
        address = Address.get_byid(address_id)
        status = UserStatus.get_byuser(address.user)
        address.is_default = False
        if status and status.default_address:
            address.is_default = status.default_address.id == address.id
        return address

    @classmethod
    def get_all_address(cls, user_id):
        address_qs = Address.search(user=user_id)
        status = UserStatus.get_byuser(user_id)
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
            cls.update_default_address(address.user, address)
        return address
