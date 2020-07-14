# coding=UTF-8

from abs.middleground.business.user.models import User


class UserServer(object):

    @classmethod
    def create(cls, **user_infos):
        user = User.create(**user_infos)
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
        for obj in obj_list:
            user = user_mapping.get(obj.user_id, None)
            obj.user = user
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
