# coding=UTF-8
import os
import io
import time
import random
import base64
import datetime
import json
import requests
from io import BytesIO
from PIL import ImageFont, Image, ImageDraw
from abs.services.agent.contract.models import Template, TemplateParam
from abs.services.crm.contract.utils.constant import KeyType
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
        back_path_mapping = {}
        for back_path in back_path_list:
            back_path_mapping[back_path["page_number"]] = back_path["path_url"]
        param_mapping = {}
        for page, path in back_path_mapping.items():
            param_mapping[page] = {
                "back_path":path,
                "word_config":[],
                "img_config":[]
            }
        for template_param in param_list:
            if template_param.page_number in param_mapping:
                if template_param.param["key_type"] == KeyType.TEXT:
                    if not template_param.value and \
                    "system" in template_param.param["name_key"]:
                        template_param.value = \
                            self.get_system_value(template_param.param["name_key"])
                    param_mapping[template_param.page_number]["word_config"].append(
                        {
                            'font_file': self.get_font_file(),
                            'font_size': self.get_font_size(),
                            'width': int(template_param.coordinate_x),
                            'height':  int(template_param.coordinate_y) + 25,
                            'color_tup': (0, 0, 0),
                            'word': template_param.value
                        },
                    )
                elif template_param.param["key_type"] == KeyType.IMGAGE:
                    if "data:image/png;base64" in template_param.value:
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

    def generate_order_contract_img(self, template, param_list):
        config_list = []
        back_path_list = json.loads(template.background_img_url)
        config_list = self.get_config_list(param_list, back_path_list)
        contract_back_url_list = image_process.save_img(
            config_list
        )
        return contract_back_url_list

    def autograph(self, contract, param_list):
        config_list = []
        back_path_list = []
        img_url_list = json.loads(contract.img_url)
        for index, back_path in enumerate(img_url_list):
            back_path_list.append({
                "page_number":index + 1,
                "path_url":back_path
            })
        config_list = self.get_config_list(param_list, back_path_list)
        contract_url, contract_img_url_list = image_process.save_pdf(
            config_list
        )
        return contract_url, contract_img_url_list

    def get_system_value(self, name_key):
        value = ""
        name_key_list = name_key.split(".")
        leng = len(name_key_list)
        if name_key_list[0] == "system":
            if leng == 2:
                if name_key_list[1] == "number":
                    value = self.generate_number()
        return value

    def get_contract_value(self, order, agent, name_key):
        value = ""
        name_key_list = name_key.split(".")
        leng = len(name_key_list)
        if name_key_list[0] == "agent":
            if leng == 2:
                value = getattr(agent, name_key_list[1])
        elif  name_key_list[0] == "order":
            if leng == 3:
                value = getattr(getattr(order, name_key_list[1]), name_key_list[2])
        return value


contract_middleware = ContractMiddleware()
