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
            company_name,
            official_seal,
            autograph_base64_image,
            name
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

        back_image_path = os.path.join(path, 'contract.png')
        font_file = os.path.join(path, 'simsun.ttc')

        word_config_list = [
            {
                'font_file': font_file,
                'font_size': 32,
                'width': 210,
                'height': 205,
                'color_tup': (0, 0, 0),
                'word': company_name
            },
            {
                'font_file': font_file,
                'font_size': 32,
                'width': 210,
                'height': 255,
                'color_tup': (0, 0, 0),
                'word': name
            }
        ]
        img_config_list = [
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
        contract_url, contract_img_url = image_process.add(
            back_image_path,
            word_config_list,
            img_config_list
        )
        return autograph_url, contract_url, contract_img_url


image_middleware = ImageMiddleware()
