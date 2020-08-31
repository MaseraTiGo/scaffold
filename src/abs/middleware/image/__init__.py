# coding=UTF-8
import os
import base64
import datetime
from io import BytesIO
from .process import image_process
from abs.middleware.file import file_middleware
from abs.middleware.config import config_middleware
from infrastructure.utils.common.convertrmb import convert_rmb_util
from abs.middleware.oss.apihelper import OSSAPI


class ImageMiddleware(object):

    def get_image(self, base64_image):
        info_list = base64_image.split(',')
        if len(info_list) == 2:
            base64_image = info_list[1]
        file_byte = base64.b64decode(base64_image)
        file_io = BytesIO(file_byte)
        return file_io

    def get_domain(self):
        return config_middleware.get_value("common", "domain")

    def get_contract(
            self,
            number,
            company_name,
            contacts_name,
            contacts_phone,
            official_seal,
            name,
            identification,
            brand_name,
            production_name,
            school_name,
            major_name,
            price
    ):

        company_official_seal = self.get_image(official_seal)
        company_official_seal = image_process.update_img_size(
            company_official_seal,
            220,
            220
        )
        path = os.path.dirname(os.path.realpath(__file__))
        font_file = os.path.join(path, 'simsun.ttc')

        config_list = [
            {
                'back_path': 'https://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/contract/template/background_1.jpg',
                'word_config': [
                    {
                        'font_file': font_file,
                        'font_size': 40,
                        'width': 1680,
                        'height': 390,
                        'color_tup': (0, 0, 0),
                        'word': number
                    },
                    # {
                    #     'font_file': font_file,
                    #     'font_size': 32,
                    #     'width': 210,
                    #     'height': 205,
                    #     'color_tup': (0, 0, 0),
                    #     'word': company_name
                    # },
                    {
                        'font_file': font_file,
                        'font_size': 50,
                        'width': 520,
                        'height': 687,
                        'color_tup': (0, 0, 0),
                        'word': name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 50,
                        'width': 1068,
                        'height': 687,
                        'color_tup': (0, 0, 0),
                        'word': identification
                    },
                    {
                        'font_file': font_file,
                        'font_size': 50,
                        'width': 649,
                        'height': 1517,
                        'color_tup': (0, 0, 0),
                        'word': brand_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 50,
                        'width': 649,
                        'height': 1592,
                        'color_tup': (0, 0, 0),
                        'word': production_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 50,
                        'width': 649,
                        'height': 1666,
                        'color_tup': (0, 0, 0),
                        'word': school_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 50,
                        'width': 649,
                        'height': 1743,
                        'color_tup': (0, 0, 0),
                        'word': major_name
                    }
                ],
                'img_config': []
            },
            {
                'back_path': 'https://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/contract/template/background_2.jpg',
                'word_config': [
                    {
                        'font_file': font_file,
                        'font_size': 50,
                        'width': 1605,
                        'height': 1071,
                        'color_tup': (0, 0, 0),
                        'word': str(price)
                    },
                    {
                        'font_file': font_file,
                        'font_size': 50,
                        'width': 445,
                        'height': 1147,
                        'color_tup': (0, 0, 0),
                        'word': convert_rmb_util.cwchange(price)
                    },
                    # {
                    #     'font_file': font_file,
                    #     'font_size': 50,
                    #     'width': 562,
                    #     'height': 2660,
                    #     'color_tup': (0, 0, 0),
                    #     'word': contacts_name
                    # },
                    # {
                    #     'font_file': font_file,
                    #     'font_size': 50,
                    #     'width': 712,
                    #     'height': 2805,
                    #     'color_tup': (0, 0, 0),
                    #     'word': contacts_phone
                    # },
                    {
                        'font_file': font_file,
                        'font_size': 50,
                        'width': 517,
                        'height': 2957,
                        'color_tup': (0, 0, 0),
                        'word': datetime.date.today().strftime('%Y.%m.%d')
                    }
                ],
                'img_config': [
                    {
                        'width': 860,
                        'height': 2610,
                        'image_path': company_official_seal
                    }
                ]
            }
        ]
        contract_back_url_list = image_process.save_img(
            config_list
        )
        return contract_back_url_list

    def autograph(self, name, phone, autograph_base64_image, contract_img_url_list):
        path = os.path.dirname(os.path.realpath(__file__))
        font_file = os.path.join(path, 'simsun.ttc')

        autograph_f = self.get_image(autograph_base64_image)
        autograph_f = image_process.update_img_size(
            autograph_f,
            250,
            150
        )
        store_name = image_process.get_store_name('autograph', '.png')
        autograph_url = OSSAPI().put_object(
            store_name,
            autograph_f.getvalue(),
            "orgdeer"
        )

        config_list = []
        for img_url in contract_img_url_list:
            config_list.append(
                {
                    'back_path': img_url,
                    'word_config': [],
                    'img_config': []
                }
            )
        config_list[-1].update({
            'word_config': [
                {
                    'font_file': font_file,
                    'font_size': 50,
                    'width': 1770,
                    'height': 2657,
                    'color_tup': (0, 0, 0),
                    'word': name
                },
                {
                    'font_file': font_file,
                    'font_size': 50,
                    'width': 1820,
                    'height': 2800,
                    'color_tup': (0, 0, 0),
                    'word': phone
                },
                {
                    'font_file': font_file,
                    'font_size': 50,
                    'width': 1690,
                    'height': 2957,
                    'color_tup': (0, 0, 0),
                    'word': datetime.date.today().strftime('%Y.%m.%d')
                }
            ],
            'img_config': [
                {
                    'width': 1710,
                    'height': 2430,
                    'image_path': autograph_f
                }
            ]
        })
        contract_url, contract_img_url_list = image_process.save_pdf(
            config_list
        )
        return autograph_url, contract_url, contract_img_url_list


image_middleware = ImageMiddleware()
