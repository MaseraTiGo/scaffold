# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.crm.university.models import School, Major, Relations


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
        if 'name' in search_info:
            search_info.update({
                'name__contains': search_info.pop('name')
            })
        school_qs = cls.search_all_school(**search_info).\
                    order_by("-is_hot", "-create_time")
        splitor = Splitor(current_page, school_qs)
        return splitor

    @classmethod
    def search_all_school(cls, **search_info):
        school_qs = School.search(**search_info)
        return school_qs

    @classmethod
    def search_hot_school(cls, **search_info):
        search_info.update({'is_hot': True})
        return cls.search_all_school(**search_info).order_by('-create_time')

    @classmethod
    def is_exsited_school(cls, name, school = None):
        school_qs = cls.search_all_school(name = name)
        if school is not None:
            school_qs = school_qs.exclude(id = school.id)
        if school_qs.count() > 0:
            return True
        return False

    @classmethod
    def search_school_id_list(cls, **search_info):
        return list(cls.search_all_school(**search_info).values_list('id', flat=True))

    @classmethod
    def update_school(cls, school, **update_info):
        if cls.is_exsited_school(update_info["name"], school):
            raise BusinessError("学校名字已存在")
        school.update(**update_info)
        return school

    @classmethod
    def hung_school(cls, obj_list):
        school_id_list = [obj.school_id for obj in obj_list]
        school_list = School.search(id__in = school_id_list)
        mapping = {}
        for school in school_list:
            mapping.update({
                school.id: school
            })
        for obj in obj_list:
            school = mapping.get(obj.school_id)
            obj.school = school

    @classmethod
    def get_location(cls, **search_info):
        return list(set(cls.search_all_school(**search_info).values_list('city', flat=True)))

    @classmethod
    def hung_major(cls, obj_list):
        major_id_list = [obj.major_id for obj in obj_list]
        major_list = Major.search(id__in = major_id_list)
        mapping = {}
        for major in major_list:
            mapping.update({
                major.id: major
            })
        for obj in obj_list:
            major = mapping.get(obj.major_id)
            obj.major = major

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
        if 'name' in search_info:
            name = search_info.pop('name')
            search_info.update({'name__contains': name})
        major_qs = Major.query().filter(**search_info)
        return major_qs

    @classmethod
    def search_hot_major(cls, **search_info):
        search_info.update({'is_hot': True})
        return cls.search_all_major(**search_info).order_by("-create_time")

    @classmethod
    def is_exsited_major(cls, name, major = None):
        major_qs = cls.search_all_major(name = name)
        if major is not None:
            major_qs = major_qs.exclude(id = major.id)
        if major_qs.count() > 0:
            return True
        return False

    @classmethod
    def update_major(cls, major, **update_info):
        if cls.is_exsited_major(update_info["name"], major):
            raise BusinessError("学校名字已存在")
        major.update(**update_info)
        return major


class UniversityRelationsServer(BaseManager):

    @classmethod
    def create(cls, **relations_info):
        relations = Relations.create(**relations_info)
        return relations

    @classmethod
    def get(cls, relations_id):
        relations = Relations.get_byid(relations_id)
        if relations is None:
            raise BusinessError("此学校专业不存在")
        return relations

    @classmethod
    def search(cls, current_page, **search_info):
        relations_qs = cls.search_all(**search_info).\
                       order_by("-create_time")
        splitor = Splitor(current_page, relations_qs)
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        if 'city' in search_info:
            city = search_info.pop('city')
            search_info.update({
                'school__city': city
            })
        if 'province' in search_info:
            province = search_info.pop('province')
            search_info.update({
                'school__province': province
            })
        relations_qs = Relations.search(**search_info)
        return relations_qs

    @classmethod
    def update(cls, relations_id, **update_info):
        relations = cls.get(relations_id)
        relations.update(**update_info)
        return relations

    @classmethod
    def remove(cls, relations_id):
        relations = cls.get(relations_id)
        relations.delete()
        return True

    @classmethod
    def is_exsited(cls, school, major, relations = None):
        relations_qs = cls.search_all(
            school = school,
            major = major
        )
        if relations is not None:
            relations_qs = relations_qs.exclude(id = relations.id)
        if relations_qs.count() > 0:
            return True
        return False

    @classmethod
    def search_all_major_list(cls, **search_info):
        return cls.search_all(
            **search_info
        ).values_list(
            'major_id',
            flat=True
        ).distinct()
