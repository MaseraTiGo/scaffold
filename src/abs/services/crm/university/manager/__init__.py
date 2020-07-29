# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.crm.university.models import School
from abs.services.crm.university.models import Major


class UniversityServer(BaseManager):

    @classmethod
    def create_school(cls, **search_info):
        school = School.create(**search_info)
        return school

    @classmethod
    def get_school(cls, school_id):
        school = School.get_byid(school_id)
        if school is None:
            raise BusinessError("此学校不存在")
        return school

    @classmethod
    def search_school(cls, current_page, **search_info):
        school_qs = cls.search_all_school(**search_info).\
                    order_by("-is_hot", "-create_time")
        splitor = Splitor(current_page, school_qs)
        return splitor

    @classmethod
    def search_all_school(cls, **search_info):
        school_qs = School.search(**search_info)
        return school_qs

    @classmethod
    def is_exsited_school(cls, name, school=None):
        school_qs = cls.search_all_school(name=name)
        if school is not None:
            school_qs = school_qs.exclude(id=school.id)
        if school_qs.count() > 0:
            return True
        return False

    @classmethod
    def update_school(cls, school, **update_info):
        if cls.is_exsited_school(update_info["name"], school):
            raise BusinessError("学校名字已存在")
        school.update(**update_info)
        return school

    @classmethod
    def create_major(cls, **search_info):
        major = Major.create(**search_info)
        return major

    @classmethod
    def get_major(cls, major_id):
        major = Major.get_byid(major_id)
        if major is None:
            raise BusinessError("此专业不存在")
        return major

    @classmethod
    def search_major(cls, current_page, **search_info):
        major_qs = cls.search_all_major(**search_info).\
                    order_by("-is_hot", "-create_time")
        splitor = Splitor(current_page, major_qs)
        return splitor

    @classmethod
    def search_all_major(cls, **search_info):
        major_qs = Major.search(**search_info)
        return major_qs

    @classmethod
    def is_exsited_major(cls, name, major=None):
        major_qs = cls.search_all_major(name=name)
        if major is not None:
            major_qs = major_qs.exclude(id=major.id)
        if major_qs.count() > 0:
            return True
        return False

    @classmethod
    def update_major(cls, major, **update_info):
        if cls.is_exsited_major(update_info["name"], major):
            raise BusinessError("学校名字已存在")
        major.update(**update_info)
        return major