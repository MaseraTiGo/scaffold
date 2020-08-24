# coding=UTF-8
import os
import base64
import datetime
from io import BytesIO
from .process import image_process
from abs.middleware.file import file_middleware
from abs.middleware.config import config_middleware


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
            phone,
            price
    ):
        path = os.path.dirname(os.path.realpath(__file__))
        company_official_seal = self.get_image(official_seal)
        company_official_seal = image_process.update_img_size(
            company_official_seal,
            220,
            220
        )

        font_file = os.path.join(path, 'simsun.ttc')

        config_list = [
            {
                'back_path': 'http://education.bq.com/resource/contract/template/background_1.jpg',
                'word_config': [
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 1660,
                        'height': 380,
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
                        'font_size': 60,
                        'width': 503,
                        'height': 680,
                        'color_tup': (0, 0, 0),
                        'word': name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 1068,
                        'height': 680,
                        'color_tup': (0, 0, 0),
                        'word': identification
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 649,
                        'height': 1070,
                        'color_tup': (0, 0, 0),
                        'word': brand_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 649,
                        'height': 1590,
                        'color_tup': (0, 0, 0),
                        'word': production_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 649,
                        'height': 1670,
                        'color_tup': (0, 0, 0),
                        'word': school_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 649,
                        'height': 1745,
                        'color_tup': (0, 0, 0),
                        'word': major_name
                    }
                ],
                'img_config': []
            },
            {
                'back_path': 'http://education.bq.com/resource/contract/template/background_2.jpg',
                'word_config': [
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 1599,
                        'height': 1075,
                        'color_tup': (0, 0, 0),
                        'word': str(price)
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 562,
                        'height': 2670,
                        'color_tup': (0, 0, 0),
                        'word': contacts_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 612,
                        'height': 2810,
                        'color_tup': (0, 0, 0),
                        'word': contacts_phone
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 517,
                        'height': 2950,
                        'color_tup': (0, 0, 0),
                        'word': str(datetime.date.today().year)
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 640,
                        'height': 2950,
                        'color_tup': (0, 0, 0),
                        'word': str(datetime.date.today().month)
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 740,
                        'height': 2950,
                        'color_tup': (0, 0, 0),
                        'word': str(datetime.date.today().day)
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 1766,
                        'height': 2510,
                        'color_tup': (0, 0, 0),
                        'word': name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 1794,
                        'height': 2630,
                        'color_tup': (0, 0, 0),
                        'word': name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 1847,
                        'height': 2775,
                        'color_tup': (0, 0, 0),
                        'word': phone
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 1684,
                        'height': 2950,
                        'color_tup': (0, 0, 0),
                        'word': str(datetime.date.today().year)
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 1797,
                        'height': 2950,
                        'color_tup': (0, 0, 0),
                        'word': str(datetime.date.today().month)
                    },
                    {
                        'font_file': font_file,
                        'font_size': 60,
                        'width': 1900,
                        'height': 2950,
                        'color_tup': (0, 0, 0),
                        'word': str(datetime.date.today().day)
                    },
                ],
                'img_config': [
                    {
                        'width': 350,
                        'height': 3000,
                        'image_path': company_official_seal
                    }
                ]
            }
        ]
        contract_back_url_list = image_process.save_img(
            config_list
        )
        return contract_back_url_list

    def autograph(self, autograph_base64_image, contract_img_url_list):
        autograph_f = self.get_image(autograph_base64_image)
        autograph_url = file_middleware.save(
            '.png',
            autograph_f,
            'autograph'
        )
        autograph_f = image_process.update_img_size(
            autograph_f,
            250,
            150
        )
        config_list = []
        domain = self.get_domain()
        for img_url in contract_img_url_list:
            config_list.append(
                {
                    'back_path': domain + img_url,
                    'word_config': [],
                    'img_config': []
                }
            )
        config_list[-1]['img_config'] = [
            {
                'width': 1100,
                'height': 3020,
                'image_path': autograph_f
            }
        ]
        contract_url, contract_img_url_list = image_process.save_pdf(
            config_list
        )
        return autograph_url, contract_url, contract_img_url_list


image_middleware = ImageMiddleware()
