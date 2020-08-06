# coding=UTF-8
import os
from .process import image_process


class ImageMiddleware(object):

    def get_contract(self):
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
                'word': '舒文俊'
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
                'image_path': os.path.join(path, 'word.jpg')
            }
        ]
        image_process.add(
            back_image_path,
            word_config_list,
            img_config_list
        )


image_middleware = ImageMiddleware()
