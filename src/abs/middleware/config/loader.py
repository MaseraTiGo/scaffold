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
        self.set_value('common', 'domain', '域名')

        self.set_key('alipay', '支付宝')
        self.set_value('alipay', 'appid', '支付宝appid', default = "2021001190655174")

        self.set_key('wechat_merchant', '微信商户')
        self.set_value('wechat_merchant', 'mchid', '微信mchid', default = "1602241032")
        self.set_value('wechat_merchant', 'key', '微信key', default = "chenglu20200827chenglu20200827cl")

        self.set_key('wechat_clzj_mini', '成录之家小程序')
        self.set_value('wechat_clzj_mini', 'appid', '微信appid', default = "wxe9f91431bf96d1f4")
        self.set_value('wechat_clzj_mini', 'appsecret', '微信appsecret', default = "29bb71b60211c72bc32b6a2a42556be1")

        self.set_key('wechat_cl_app', '橙鹿app')
        self.set_value('wechat_cl_app', 'appid', '微信APPappid', default = "wx8aa0090b4ffd643f")
        self.set_value('wechat_cl_app', 'appsecret', '微信APPappsecret', default = "06312ddcbfb17e74d213759db95dc34a")

        self.set_key('email', '邮件配置')
        self.set_value('email', 'sender', '邮件发送方email', default = "orgdeer@cljykjhbwwgc.onexmail.com")
        self.set_value('email', 'account', '邮件发送方账号', default = "orgdeer@cljykjhbwwgc.onexmail.com")
        self.set_value('email', 'passwd', '邮件发送方密码', default = "zxcde321CL")
        self.set_value('email', 'host', 'SMTP服务器主机', default = "smtp.exmail.qq.com")
        self.set_value('email', 'port', 'SMTP服务使用的端口号', default = "465")

        self.set_key('saobei', '扫呗配置')
        self.set_value('saobei', 'terminal_id', '终端号码', default = "11972386")
        self.set_value('saobei', 'merchant_no', '商户号', default = "852108299000137")
        self.set_value('saobei', 'order_body', '订单描述', default = "缴费")
        self.set_value('saobei', 'access_token', '支付access_token', default = "fdcb0604199c48a4b3fdfc01773922e9")
        self.set_value('saobei', 'fromal_url', '请求连接', default = "http://pay.lcsw.cn/lcsw")

        self.set_key('jpush', '极光推送配置')
        self.set_value('jpush', 'app_key', '极光推送appkey', default = "f49ba8db36ec204fbaca066b")
        self.set_value('jpush', 'master_secret', '极光推送secret', default = "7d2984b05ac1a7340f803e88")


