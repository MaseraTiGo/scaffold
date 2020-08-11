# coding=UTF-8
import io
from PIL import ImageFont, Image, ImageDraw
from abs.middleware.file import file_middleware


class ImageProcess(object):

    def update_img_size(self, old_img, width, height):
        obj = Image.open(old_img)
        img = obj.resize((width, height), Image.ANTIALIAS)
        byte_io = io.BytesIO()
        img.save(byte_io, format='png')
        return byte_io

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

        file_path, save_path = file_middleware.get_save_path(
            '.pdf',
            'contract'
        )
        back_img.convert('RGB').save(
            file_path,
            'PDF',
            resolution=100.0,
            save_all=True,
            append_images=[]
        )
        img_file_path, img_save_path = file_middleware.get_save_path(
            '.png',
            'contract_img'
        )
        back_img.save(img_file_path)
        return save_path, img_save_path


image_process = ImageProcess()
