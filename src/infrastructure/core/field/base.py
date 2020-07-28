# coding=UTF-8

import json
import datetime
import re

from infrastructure.utils.common.dictwrapper import DictWrapper
from infrastructure.core.exception.debug_error import DebugError


class BaseField(object):

    def __init__(self,desc,choices=None,is_required=True,default=None,\
                 reprocess=None):
        self._desc=desc
        self._choices=choices
        self._default=default
        self._is_required=is_required
        self._choice_mapping=dict(self._choices) if self._choices else None
        if reprocess is None:
            self._reprocess=[]
        else:
            self._reprocess=reprocess if type(reprocess)==list else [reprocess]

    def json_loads(self,value):
        try:
            value=json.loads(value)
        except Exception as e:
            raise Exception("parmaster is not json data")
        else:
            return value

    def _check_choices(self,value):
        if self._choice_mapping:
            if value not in self._choice_mapping:
                print('paramter is not in choices')
                raise NotImplementedError('paramter is not in choices')
        return value

    def get_type(self):
        return self.__class__.__name__.lower().replace("field","")

    def get_desc(self):
        return self._desc

    def get_choices(self):
        return self._choices

    def is_required(self):
        return self._is_required

    def get_default(self):
        return self._default

    def parse_before(self,value):
        return value

    def parsing(self,value):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def parse_after(self,value):
        return self._check_choices(value)

    def parse(self,value):
        value=self.parse_before(value)
        value=self.parsing(value)
        value=self.parse_after(value)
        return value

    def format_before(self,value):
        return value

    def formatting(self,value):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def format_after(self,value):
        value=self._check_choices(value)
        return value

    def reprocess(self,value):
        result=value
        if self._reprocess:
            for func in self._reprocess:
                result=func(result)
        return result

    def format(self,value):
        value=self.format_before(value)
        value=self.formatting(value)
        value=self.format_after(value)
        return value


class BooleanField(BaseField):

    def parsing(self,value):
        if int(value)>0:
            return True
        else:
            return False

    def formatting(self,value):
        if value:
            return 1
        else:
            return 0


class CharField(BaseField):

    def parsing(self,value):
        return str(value)

    def formatting(self,value):
        if value is None:
            return ""
        return str(value)


class IntField(BaseField):

    def parsing(self,value):
        if value=="":
            return 0
        return int(value)

    def formatting(self,value):
        result=0
        try:
           result=int(value)
        except Exception as e:
            pass
        return result


class FloatField(BaseField):

    def parsing(self,value):
        return float(value)

    def formatting(self,value):
        return float(value)


class DateField(BaseField):

    def parsing(self,value):
        value_time=datetime.datetime.strptime(value,'%Y-%m-%d')
        value_time_day=datetime.date(value_time.year,value_time.month,value_time.day)
        return value_time_day

    def formatting(self,value):
        if not isinstance(value,datetime.date):
            return None
            # raise DebugError()
        return value.strftime('%Y-%m-%d')


class DatetimeField(BaseField):

    def parsing(self,value):
        try:
            datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
        except exception as e:
            print(e)
        return datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S")

    def formatting(self,value):
        if not isinstance(value,datetime.datetime):
            return None
            # raise DebugError()
        return value.strftime("%Y-%m-%d %H:%M:%S")


class DictField(BaseField):

    def __init__(self,conf,*args,**kwargs):
        super(DictField,self).__init__(*args,**kwargs)

        if type(conf) is not dict:
            raise Exception("DictField need dict type value")

        for key,value in conf.items():
            if not isinstance(value,BaseField):
                raise Exception("DictField is just to load BaseField")
            setattr(self,key,value)

    def get_fields(self):
        if not hasattr(self,'_fields'):
            self._fields={key: value for key,value in self.__dict__.items() if
                            isinstance(value,BaseField)}
        return self._fields

    def parsing(self,value):
        if type(value) is str:
            value=self.json_loads(value)

        if type(value) is dict:
            fields=self.get_fields()
            result={}
            for key,helper in fields.items():
                if key not in value:
                    if helper._is_required:
                        raise Exception("paramter '{}' losted".format(key))
                    else:
                        continue

                try:
                    cur_value=helper.parsing(value[key])
                except Exception as e:
                    raise Exception("paramter '{}' format error".format(key))
                else:
                    result[key]=cur_value
            return DictWrapper(result)

        raise Exception("paramter is not dict")

    def formatting(self,value):
        if type(value) is not dict:
            raise Exception("paramter is not dict")

        fields=self.get_fields()
        result={}
        for key,helper in fields.items():
            if key not in value:
                if self._is_required:
                    raise Exception("paramter '{}' losted".format(key))
                else:
                    continue

            try:
                cur_value=helper.formatting(value[key])
            except Exception as e:
                raise Exception("paramter '{}' format error, e = {}".format(key,e))
            else:
                result[key]=cur_value
        return DictWrapper(result)

    def reprocess(self,value):
        fields=self.get_fields()
        result={}
        for key,helper in fields.items():
            if key not in value:
                continue

            try:
                cur_value=helper.reprocess(value[key])
            except Exception as e:
                raise Exception("paramter '{}' format error, e = {}".format(key,e))
            else:
                result[key]=cur_value
        return DictWrapper(result)


class ListField(BaseField):

    def __init__(self,fmt,*args,**kwargs):
        super(ListField,self).__init__(*args,**kwargs)
        self._fmt=fmt

    def get_fmt(self):
        return self._fmt

    def parsing(self,value):
        if type(value) is str:
            value=self.json_loads(value)

        if type(value) is list:
            return [self._fmt.parsing(cur_value) for cur_value in value]

        raise Exception("paramter is not list")

    def formatting(self,value):
        if type(value) is not list:
            raise Exception("paramter is not list")

        return [self._fmt.formatting(cur_value) for cur_value in value]

    def reprocess(self,value):
        return [self._fmt.reprocess(cur_value) for cur_value in value]


class FileField(BaseField):

    def parsing(self,value):
        return value

    def formatting(self,value):
        return value


class MobileField(BaseField):

    def parsing(self,value):
        return str(value)

    def formatting(self,value):
        if value:
            p=re.compile(r'(\d{3})(\d{4})(\d{4})')
            value=p.sub(r'\1****\3',value)
        return value


class HideField(BaseField):

    def parsing(self,value):
        return str(value)

    def formatting(self,value):
        if value:
            hide_str=value[6:-4]
            value=re.sub(hide_str,len(hide_str)*'*',value)
        return value

