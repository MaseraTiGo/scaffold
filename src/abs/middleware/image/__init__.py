# coding=UTF-8
import os
import base64
from mimetypes import guess_extension, guess_type
from io import BytesIO
from .process import image_process
from abs.middleware.file import file_middleware


class ImageMiddleware(object):

    def get_image(self, base64_image):
        # info_list = base64_image.split(',')
        # extension_name = guess_extension(info_list[0])
        extension_name = '.png'
        file_byte = base64.b64decode(base64_image)
        file_io = BytesIO(file_byte)
        autograph = file_middleware.save(extension_name, file_io, 'autograph')
        return autograph, file_io

    def get_contract(self, autograph_base64_image, name):
        autograph_url, f = self.get_image(autograph_base64_image)
        path = os.path.dirname(os.path.realpath(__file__))
        back_image_path = os.path.join(path, 'contract.png')
        font_file = './simsun.ttc'
        word_config_list = [
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
                'width': 400,
                'height': 3000,
                'image_path': os.path.join(path, 'company.png')
            },
            {
                'width': 1100,
                'height': 3000,
                'image_path': f
            }
        ]
        contract_url = image_process.add(
            back_image_path,
            word_config_list,
            img_config_list
        )
        return autograph_url, contract_url


image_middleware = ImageMiddleware()
