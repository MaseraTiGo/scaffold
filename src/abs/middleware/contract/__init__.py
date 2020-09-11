# coding=UTF-8
import os
import io
import time
import random
import base64
import datetime
import json
import requests
from PIL import ImageFont, Image, ImageDraw
from abs.services.agent.contract.models import Template, TemplateParam
from abs.services.crm.contract.utils.contact import KeyType
from abs.middleware.image.process import image_process


class ContractMiddleware(object):


    def generate_number(self):
        return 'Sn_200' + str(int(time.time())) + \
                str(random.randint(10000, 99999))

    def get_font_size(self):
        return 50

    def get_font_file(self):
        path = os.path.dirname(os.path.realpath(__file__))
        font_file = os.path.join(path, 'simsun.ttc')
        return font_file

    def update_img_size(self, old_img, width, height):
        obj = Image.open(old_img)
        img = obj.resize((width, height), Image.ANTIALIAS)
        byte_io = io.BytesIO()
        img.save(byte_io, format = 'png')
        return byte_io

    def get_base64_img(self, base64_image):
        info_list = base64_image.split(',')
        if len(info_list) == 2:
            base64_image = info_list[1]
        file_byte = base64.b64decode(base64_image)
        file_io = BytesIO(file_byte)
        return file_io

    def get_img_byurl(self, img_url):
        response = requests.get(img_url)
        response = response.content
        byte_io = io.BytesIO()
        byte_io.write(response)
        return byte_io

    def get_config_list(self, param_list, back_path_list):
        param_mapping = {}
        for template_param in param_list:
            template_param.param = json.loads(template_param.content)
            if template_param.page_number not in param_mapping:
                param_mapping[template_param.page_number] = {
                    "back_path":back_path_list[template_param.page_number - 1],
                    "word_config":[],
                    "img_config":[]
                }
            if template_param.param["key_type"] == KeyType.TEXT:
                param_mapping[template_param.page_number]["word_config"].append(
                    {
                        'font_file': self.get_font_file(),
                        'font_size': self.get_font_size(),
                        'width': int(template_param.coordinate_x),
                        'height':  int(template_param.coordinate_y),
                        'color_tup': (0, 0, 0),
                        'word': template_param.value
                    },
                )
            elif template_param.param["key_type"] == KeyType.IMGAGE:
                if template_param.param["name_key"] == "official_seal":
                    img = self.get_base64_img(template_param.value)
                else:
                    img = self.get_img_byurl(template_param.value)
                param_mapping[template_param.page_number]["img_config"].append(
                    {
                        'width': int(template_param.coordinate_x),
                        'height':  int(template_param.coordinate_y),
                        'image_path':self.update_img_size(
                            img,
                            int(template_param.width),
                            int(template_param.height)
                        )
                    },
                )
        config_list = list(param_mapping.values())
        return config_list

    def generate_order_contract_img(self, agent, mg_order, template, param_list):
        config_list = []
        back_path_list = json.loads(template.background_img_url)
        config_list = self.get_config_list(param_list, back_path_list)
        contract_back_url_list = image_process.save_img(
            config_list
        )
        return contract_back_url_list

    def autograph(self, param_list, back_path_list):
        pass

contract_middleware = ContractMiddleware()
