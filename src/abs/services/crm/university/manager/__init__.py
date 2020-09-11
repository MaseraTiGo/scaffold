# coding=UTF-8

from infrastructure.core.exception.business_error import BusinessError
from infrastructure.utils.common.split_page import Splitor

from abs.common.manager import BaseManager
from abs.services.crm.university.models import School, Major, Relations
from abs.middleground.business.production.manager import ProductionServer
from abs.middleground.business.merchandise.manager import MerchandiseServer
from abs.services.crm.university.models import School, Major, Relations, Years


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
        return list(cls.search_all_school(**search_info).values_list('id', flat = True))

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
        return cls.search_all_school(
            **search_info
        ).values(
            'province',
            'city'
        ).distinct()

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

    @classmethod
    def remove_major(cls, major_id):
        major = cls.get_major(major_id)
        relations_qs = UniversityRelationsServer.search_all(major = major)
        if relations_qs.count() > 0:
            raise BusinessError("专业已绑定学校禁止删除")
        major.delete()
        return True


class UniversityRelationsServer(BaseManager):

    @classmethod
    def create(cls, **relations_info):
        if cls.is_exsited(
            relations_info["school"],
            relations_info["major"],
        ):
            raise BusinessError("此学校专业已存在")
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
        if 'major_name' in search_info:
            major_name = search_info.pop('major_name')
            search_info.update({
                'major__name__contains': major_name
            })
        relations_qs = Relations.search(**search_info)
        return relations_qs

    @classmethod
    def update(cls, relations_id, **update_info):
        relations = cls.get(relations_id)
        if cls.is_exsited(
            relations.school,
            update_info["major"],
            relations,
        ):
            raise BusinessError("此学校专业已存在")
        relations.update(**update_info)
        return relations

    @classmethod
    def remove(cls, relations_id):
        relations = cls.get(relations_id)
        years_qs = UniversityYearsServer.search_all(
            relations = relations
        )
        if years_qs.count() > 0:
            raise BusinessError("存在学年无法删除")
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
            flat = True
        ).order_by(
            '-major__is_hot',
            'major__create_time'
        ).distinct()

    @classmethod
    def search_major_list(cls, current_page, **search_info):
        splitor = Splitor(
            current_page,
            cls.search_all_major_list(**search_info)
        )
        return splitor


class UniversityYearsServer(BaseManager):

    @classmethod
    def create(cls, **years_info):
        if cls.is_exsited(
            years_info["category"],
            years_info["duration"],
            years_info["relations"]
        ):
            raise BusinessError("此学年已添加")
        years = Years.create(**years_info)
        return years

    @classmethod
    def batch_create(cls, years_list, relations):
        create_list = []
        for year_dic in years_list:
            create_list.append(Years(
                unique_number = Years.generate_unique_number(),
                relations = relations,
                category = year_dic["category"],
                duration = year_dic["duration"],
            ))
        Years.objects.bulk_create(create_list)

    @classmethod
    def get(cls, years_id):
        years = Years.get_byid(years_id)
        if years is None:
            raise BusinessError("此学校专业学年不存在")
        return years

    @classmethod
    def search(cls, current_page, **search_info):
        years_qs = cls.search_all(**search_info).\
                       order_by("-create_time")
        splitor = Splitor(current_page, years_qs)
        return splitor

    @classmethod
    def search_all(cls, **search_info):
        if 'school_id' in search_info:
            school_id = search_info.pop('school_id')
            search_info.update({
                'relations__school_id': school_id
            })
        if 'major_id' in search_info:
            major_id = search_info.pop('major_id')
            search_info.update({
                'relations__major_id': major_id
            })
        years_qs = Years.search(**search_info)
        return years_qs

    @classmethod
    def linkage(cls):
        link_mapping = {}
        relations_mapping = {}
        years_qs = cls.search_all()
        for years in years_qs:
            if years.relations not in relations_mapping:
                relations_mapping[years.relations] = []
            relations_mapping[years.relations].append({
                'years_id':years.id,
                'category': years.category,
                'duration': years.duration,
            })
        for relations, years_list in relations_mapping.items():
            major_mapping = {
                'major_id':relations.major.id,
                'major_name':relations.major.name,
                'children':years_list
            }
            if relations.school not in link_mapping:
                link_mapping[relations.school] = {
                    "school_id":relations.school.id,
                    "school_name":relations.school.name,
                    "children":[]
                }
            link_mapping[relations.school]["children"].append(major_mapping)
        return list(link_mapping.values())

    @classmethod
    def update(cls, years_id, **update_info):
        years = cls.get(years_id)
        if cls.is_exsited(
            update_info["category"],
            update_info["duration"],
            years.relations,
            years
        ):
            raise BusinessError("此学年已添加")
        years.update(**update_info)
        return years

    @classmethod
    def remove(cls, years_id):
        years = cls.get(years_id)
        years.delete()
        return True

    @classmethod
    def hung_years_byrelations(cls, relations_list):
        relations_mapping = {}
        for relations in relations_list:
            relations.years_list = []
            relations_mapping[relations.id] = relations
        years_qs = cls.search_all(relations_id__in = relations_mapping.keys())
        for years in years_qs:
            if years.relations_id in relations_mapping:
                relations_mapping[years.relations_id].years_list.append(years)
        return relations_list

    @classmethod
    def hung_years(cls, obj_list):
        obj_mapping = {}
        for obj in obj_list:
            obj.years = None
            if obj.years_id not in obj_mapping:
                obj_mapping[obj.years_id] = []
            obj_mapping[obj.years_id].append(obj)
        years_qs = cls.search_all(id__in = obj_mapping.keys())
        for years in years_qs:
            if years.id in obj_mapping:
                for obj in obj_mapping[years.id]:
                    obj.years = years
        return obj_list

    @classmethod
    def is_exsited(cls, category, duration, relations, years = None):
        years_qs = cls.search_all(
            category = category,
            duration = duration,
            relations = relations
        )
        if years is not None:
            years_qs = years_qs.exclude(id = years.id)
        if years_qs.count() > 0:
            return True
        return False

    @classmethod
    def search_major_list(cls, current_page, **search_info):
        years_qs = cls.search_all(
            **search_info
        ).values_list(
            'relations__major'
            , flat = True
        ).order_by(
            '-relations__major__is_hot',
            'create_time'
        ).distinct()
        return Splitor(current_page, years_qs)

    @classmethod
    def search_school_list(cls, current_page, **search_info):
        years_qs = cls.search_all(
            **search_info
        ).values_list(
            'relations__school'
            , flat = True
        ).order_by(
            '-relations__school__is_hot',
            'create_time'
        ).distinct()
        return Splitor(current_page, years_qs)

    @classmethod
    def search_id_list(cls, **search_info):
        return list(cls.search_all(
            **search_info
        ).values_list(
            'id',
            flat = True
        ))
