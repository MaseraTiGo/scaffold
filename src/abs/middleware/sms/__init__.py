# coding=UTF-8
from infrastructure.utils.common.single import Single

from abs.middleware.extend.sms import local_sms,verify_code_sms
from .helper import CodeHelper,MessageHelper
from abs.services.crm.tool.utils.contact import SceneTypes


class SmsMiddleware(Single):
    def __init__(self):
        self._company_mapping={}
        self._template_mapping={}

    def register_company(self,company_obj):
        self._company_mapping.update({
            company_obj.label: company_obj
        })

    def get_company_mapping(self):
        return self._company_mapping

    def register_template(self,template):
        self._template_mapping.update({
            template.label: template
        })

    def get_template_mapping(self):
        return self._template_mapping

    def get_company(self,label):
        return self._company_mapping.get(label)

    def get_template(self,label):
        return self._template_mapping.get(label)

    def send_code(self,phone,scene,source_type):
        send_info=sms_middleware.get_send_info(scene)
        company=self.get_company(send_info['company_label'])
        template=self.get_template(send_info['template_label'])
        template_id=send_info['template_id']
        sign_name=send_info['sign_name']
        return CodeHelper(phone,scene).send(company,template,template_id,sign_name,source_type)

    def send_msg(self,phone,scene,unique_no,source_type,**kwargs):
        send_info=sms_middleware.get_send_info(scene)
        company=self.get_company(send_info['company_label'])
        template=self.get_template(send_info['template_label'])
        template_id=send_info['template_id']
        sign_name=send_info['sign_name']
        return MessageHelper(phone,scene,unique_no).send(company,template,template_id,sign_name,source_type,**kwargs)

    def check_code(self,phone,scene,code):
        return CodeHelper(phone,scene).check(code)

    def get_label_is_open(cls,label):
        """短信平台开关"""
        return 'yes'

    def get_scene_is_open(cls,scene):
        """短信场景开关 """
        return 'yes'

    def get_send_info(self,scene):
        send_info={
            SceneTypes.REGISTER: {
                'company_label': 'local_sms',
                'template_id': 'A003',
                'template_label': 'verify_code',
                'sign_name': '橙鹿'
            },
            SceneTypes.FORGET: {
                'company_label': 'local_sms',
                'template_id': 'A003',
                'template_label': 'verify_code',
                'sign_name': '橙鹿'
            },
            SceneTypes.BINDCARD: {
                'company_label': 'local_sms',
                'template_id': 'A003',
                'template_label': 'verify_code',
                'sign_name': '橙鹿'
            },
            SceneTypes.LOGIN: {
                'company_label': 'local_sms',
                'template_id': 'A003',
                'template_label': 'verify_code',
                'sign_name': '橙鹿'
            },
            SceneTypes.WECHAT_REGISTER: {
                'company_label': 'local_sms',
                'template_id': 'A003',
                'template_label': 'verify_code',
                'sign_name': '橙鹿'
            }
        }
        return send_info.get(scene)


sms_middleware=SmsMiddleware()
sms_middleware.register_company(local_sms)
sms_middleware.register_template(verify_code_sms)
