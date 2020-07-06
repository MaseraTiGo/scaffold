# coding=UTF-8

from infrastructure.core.field.base import ListField, DictField


class ApiDocBuilder(object):

    def __init__(self, api):
        self._api = api

    def get_api(self):
        return self._api

    def generate(self):
        raise NotImplementedError('Please imporlement this interface in subclass')


class TextApiDoc(ApiDocBuilder):

    def generate(self):
        content_list = [
            self.generate_author(),
            self.generate_version(),
            "",
        ]
        return '\n'.join([
            self.generate_author(),
            self.generate_version(),
            "",
            self.generate_desc(),
            "",
            self.generate_params(),
            "",
            self.generate_return(),
        ])

    def generate_author(self):
        return "@author : {}".format(self.get_api().get_author())

    def generate_version(self):
        return "@version : {}".format(self.get_api().get_version())

    def generate_desc(self):
        return "@desc : {}".format(self.get_api().get_desc())

    def generate_return_desc(self, field):
        fmt_str = "{} # {}"
        tmp_str = fmt_str.format(field.get_type(), field.get_desc())
        choices = field.get_choices()
        if choices:
            tmp_str += " 例：" + ' 、 '.join(" -> ".join(map(str, [key, value])) for key, value in choices)
        return tmp_str

    def generate_param_desc(self, field):
        fmt_str = "{} # {}"
        tmp_str = fmt_str.format(field.get_type(), field.get_desc())
        choices = field.get_choices()
        if choices:
            tmp_str += " 例：" + ' 、 '.join(" -> ".join(map(str, [key, value])) for key, value in choices)

        default = field.get_default()
        if default:
            tmp_str += " 默认值：" + default

        is_need = field.is_required()
        if not is_need:
            tmp_str += " (选填)"

        return tmp_str

    def generate_field(self, field, fields, level):
        fill_flag = " " * 8
        cur_flag = fill_flag * level
        next_flag = fill_flag * (level + 1)

        if isinstance(field, DictField):
            fields.append(cur_flag + '{  # ' + field.get_desc())
            for sub_name, sub_field in field.get_fields().items():
                fmt_str = next_flag + "{} : {}"
                tmp_str = fmt_str.format(sub_name, self.generate_param_desc(sub_field))
                # tmp_str = fmt_str.format(sub_name, sub_field.get_type(), sub_field.get_desc())
                fields.append(tmp_str)
                self.generate_field(sub_field, fields, level + 1)
            fields.append(cur_flag + '}')

        elif isinstance(field, ListField):
            fields.append(cur_flag + '[')
            sub_field = field.get_fmt()
            if not isinstance(sub_field, DictField) and not isinstance(sub_field, ListField):
                fmt_str = next_flag + "{} # {}"
                tmp_str = fmt_str.format(sub_field.get_type(), sub_field.get_desc())
                fields.append(tmp_str)
            else:
                self.generate_field(sub_field, fields, level + 1)
            fields.append(next_flag + '......')
            fields.append(cur_flag + ']')

    def generate_params(self):
        fmt_str = "@param : {} - {}"
        api = self.get_api()
        fields = []
        for name, field in api.get_request_fields().items():
            tmp_str = fmt_str.format(name, self.generate_param_desc(field))
            fields.append(tmp_str)

            org_field = field.get_field()
            self.generate_field(org_field, fields, level = 1)

        return '\n'.join(fields)

    def generate_return(self):
        fmt_str = "@return : {} - {}"
        api = self.get_api()
        fields = []
        for name, field in api.get_response_fields().items():
            tmp_str = fmt_str.format(name, self.generate_return_desc(field))
            org_field = field.get_field()
            fields.append(tmp_str)
            self.generate_field(org_field, fields, level = 1)

        return '\n'.join(fields)
