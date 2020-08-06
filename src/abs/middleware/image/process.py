# coding=UTF-8
import os
import time
import random
from PIL import ImageFont, Image, ImageDraw
from settings import STATIC_URL, STATICFILES_DIRS

class ImageProcess(object):

    def add(
        self,
        back_image_path,
        word_config_list,
        img_config_list
    ):
        back_img = Image.open(back_image_path)
        draw = ImageDraw.Draw(back_img)
        for config in word_config_list:
            font = ImageFont.truetype(
                config['font_file'],
                config['font_size'],
                encoding='utf-8'
            )
            position = (
                config['width'],
                config['height']
            )
            color = config['color_tup']
            draw.text(
                position,
                config['word'],
                color,
                font=font
            )
        for config in img_config_list:
            box = (
                config['width'],
                config['height']
            )
            img = Image.open(config['image_path']).convert('RGBA')
            r, g, b, a = img.split()
            back_img.paste(img, box, a)


        name = "{}_{}.jpeg".format(
            str(random.randint(1000, 9999)),
            int(time.time())
        )
        base_dir = STATICFILES_DIRS[0]
        save_path = os.path.join(base_dir, 'contract')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, name)
        url = STATIC_URL + file_path.replace(base_dir, "")
        back_img.save(url)
        return url


image_process = ImageProcess()
