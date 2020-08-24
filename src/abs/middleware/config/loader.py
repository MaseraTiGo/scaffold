# coding=UTF-8

from abs.services.crm.tool.store.config import Config

class LoaderHelper(object):

    def __init__(self):
        self.data = {}
        self.get_config_data()

    @classmethod
    def generate(cls, **attr):
        config = Config.create(**attr)
        if config is not None:
            return config
        return None

    @classmethod
    def loading(cls, **search_info):
        config_list = list(Config.objects.filter(**search_info).order_by('key'))
        for config in config_list:
            config.value_type = "text"
            config.option = []
            if config.type in LoaderHelper().data and config.key in LoaderHelper().data[config.type]['data']:
                config.value_type = LoaderHelper().data[config.type]['data'][config.key]["type"]
                config.option = LoaderHelper().data[config.type]['data'][config.key]["option"]
        return config_list

    @classmethod
    def get_config(cls, type, key):
        config_qs = Config.objects.filter(type = type, key = key)
        if config_qs:
            return config_qs[0]
        return None

    @classmethod
    def generate_config(cls, **attrs):
        return Config.create(**attrs)

    def set_key(self, key, desc):
        self.data.update({key: {'type_desc': desc, 'data': {}}})

    def set_value(self, key, value_key, name, default = '', type = 'text', option = []):
        self.data[key]['data'].update({value_key: {'name': name, 'value': default, 'type':type, 'option':option}})

    def get_config_data(self):
        self.set_key('common', '通用配置')
        self.set_value('common', 'crm_appkey', 'CRM总控公司授权appkey')
        self.set_value('common', 'agent_platform_id', 'CRM代理商端平台id')
        self.set_value('common', "is_login", '禁止登陆', default = 'no', type = 'select', option = ['yes', 'no'])
