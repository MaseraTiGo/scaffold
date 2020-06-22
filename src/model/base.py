# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

import time
import hashlib
import datetime


from django.db.models import *


class BaseModel(Model):

    unique_number = CharField(verbose_name = "唯一逻辑编码", unique = True, max_length = 64)

    class Meta:
        abstract = True


    @classmethod
    def generate_unique_number(cls):
        unque_str = cls.__name__ + str(time.time())
        return hashlib.md5(unque_str.encode(encoding='UTF-8')).hexdigest()


    @classmethod
    def create(cls, **kwargs):
        valid_keys = set(field.name for field in cls._meta.fields)
        default = {attr:val for attr, val in  kwargs.items() if attr in valid_keys}
        default.update({'unique_number': cls.generate_unique_number()})
        try:
            return cls.objects.create(**default)
        except Exception as e:
            # print("【attention】(class:{class_name}) to create error, the detail : {e}"\
            #       .format(class_name = cls.__name__, e = e))
            raise e
            return None

    @classmethod
    def get_byid(cls, id):
        try:
            relations = [field.name for field in cls.get_relateionship_fields()]
            return cls.objects.select_related(*relations).get(id = id)
        except:
            return None

    @classmethod
    def get_relateionship_fields(cls):
        return [ field for field in cls._meta.fields if isinstance(field, ForeignKey) ]

    @classmethod
    def get_valid_fieldname(cls):
        return {field.name:field for field in cls._meta.fields}

    @classmethod
    def query(cls, **search_info):
        relations = [field.name for field in cls.get_relateionship_fields()]
        valid_mapping = cls.get_valid_fieldname()
        qs = cls.objects.select_related(*relations).filter()

        for key, val in search_info.items():
            if key in valid_mapping :
                field = valid_mapping[key]
                if val or isinstance(field, BooleanField) or isinstance(field, IntegerField) :
                    temp = {}
                    if isinstance(field, AutoField):
                        temp.update({field.name : int(val)})
                    elif isinstance(field, CharField):
                        temp.update({'{}__contains'.format(field.name) : val})
                    elif isinstance(field, IntegerField):
                        temp.update({field.name : int(val)})
                    elif isinstance(field, BooleanField):
                        temp.update({field.name : bool(val)})
                    elif isinstance(field, TextField):
                        temp.update({'{}__contains'.format(field.name) : val})
                    elif isinstance(field, DateTimeField):
                        # fsy
                        temp.update({field.name : val})
                    elif isinstance(field, DateField):
                        # fsy
                        temp.update({field.name : datetime.date(val.year, val.month, val.day)})
                    elif isinstance(field, ForeignKey):
                        temp.update({field.name : val})
                    qs = qs.filter(**temp)

        return qs

    def update(self, **kwargs):
        valid_files = []
        valid_keys = self.__class__.get_valid_fieldname().keys()

        for attr, val in kwargs.items():
            if attr in valid_keys:
                setattr(self, attr, val)
                valid_files.append(attr)

        try:
            if valid_files:
                self.save()

                for attr in valid_files:
                    kwargs.pop(attr)

                # print("【attention】 (class:{class_name},obj_id={obj_id}) fields have updated, the detail : {fields_str}"\
                #       .format(class_name = self.__class__.__name__, obj_id = self.id, fields_str = ','.join(valid_files)))
            return self
        except Exception as e:
            # print("【attention】(class:{class_name},obj_id={obj_id})field to update error, the detail : {e}"\
            #       .format(class_name = self.__class__.__name__, obj_id = self.id, e = e))
            raise e
            return None
