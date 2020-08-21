# coding=UTF-8
import os
import base64
from io import BytesIO
from .process import image_process
from abs.middleware.file import file_middleware


class ImageMiddleware(object):

    def get_image(self, base64_image):
        info_list = base64_image.split(',')
        if len(info_list) == 2:
            base64_image = info_list[1]
        file_byte = base64.b64decode(base64_image)
        file_io = BytesIO(file_byte)
        return file_io

    def get_contract(
            self,
            number,
            company_name,
            contacts_name,
            contacts_phone,
            official_seal,
            autograph_base64_image,
            name,
            identification,
            brand_name,
            production_name,
            school_name,
            major_name,
            phone,
            price
    ):
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
                'back_path': 'http://test-b.rong-mi.com/resource/contract/background_1.png',
                'word_config': [
                    {
                        'font_file': font_file,
                        'font_size': 16,
                        'width': 535,
                        'height': 63,
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
                        'font_size': 18,
                        'width': 110,
                        'height': 175,
                        'color_tup': (0, 0, 0),
                        'word': name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 18,
                        'width': 295,
                        'height': 175,
                        'color_tup': (0, 0, 0),
                        'word': identification
                    },
                    {
                        'font_file': font_file,
                        'font_size': 18,
                        'width': 125,
                        'height': 455,
                        'color_tup': (0, 0, 0),
                        'word': brand_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 18,
                        'width': 125,
                        'height': 485,
                        'color_tup': (0, 0, 0),
                        'word': production_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 18,
                        'width': 125,
                        'height': 515,
                        'color_tup': (0, 0, 0),
                        'word': school_name
                    },
                    {
                        'font_file': font_file,
                        'font_size': 18,
                        'width': 125,
                        'height': 545,
                        'color_tup': (0, 0, 0),
                        'word': major_name
                    }
                ],
                'img_config': []
            },
            {
                'back_path': 'http://test-b.rong-mi.com/resource/contract/background_2.png',
                'word_config': [
                    # {
                    #
                    # }
                ],
                'img_config': [
                    {
                        'width': 350,
                        'height': 3000,
                        'image_path': company_official_seal
                    },
                    {
                        'width': 1100,
                        'height': 3020,
                        'image_path': autograph_f
                    }
                ]
            }
        ]
        contract_url, contract_img_url_list = image_process.add(
            config_list
        )
        return autograph_url, contract_url, contract_img_url_list


image_middleware = ImageMiddleware()
