# coding=UTF-8

from PIL import ImageFont, Image, ImageDraw


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
        back_img.show()


image_process = ImageProcess()
