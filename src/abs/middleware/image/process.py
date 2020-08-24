# coding=UTF-8
import io
from PIL import ImageFont, Image, ImageDraw
from abs.middleware.file import file_middleware
import urllib.request

class ImageProcess(object):

    def update_img_size(self, old_img, width, height):
        obj = Image.open(old_img)
        img = obj.resize((width, height), Image.ANTIALIAS)
        byte_io = io.BytesIO()
        img.save(byte_io, format='png')
        return byte_io

    def get_img_byurl(self, img_url):
        response = urllib.request.urlopen(img_url)
        response = response.read()
        byte_io = io.BytesIO()
        byte_io.write(response)
        return byte_io

    def process(
        self,
        config_list
    ):
        result_list = []
        for item in config_list:
            back_img = Image.open(
                self.get_img_byurl(item['back_path'])
            )

            draw = ImageDraw.Draw(back_img)

            for config in item['word_config']:
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
            for config in item['img_config']:
                box = (
                    config['width'],
                    config['height']
                )
                img = Image.open(config['image_path']).convert('RGBA')
                r, g, b, a = img.split()
                back_img.paste(img, box, a)
            result_list.append(back_img)
        return result_list

    def save_img(self, config_list):
        result_list = self.process(config_list)
        img_save_path_list = []
        for result in result_list:
            img_file_path, img_save_path = file_middleware.get_save_path(
                '.png',
                'contract_back'
            )
            result.save(img_file_path)
            img_save_path_list.append(img_save_path)
        return img_save_path_list

    def save_pdf(self, config_list):
        result_list = self.process(config_list)
        pdf_file_path, pdf_save_path = file_middleware.get_save_path(
            '.pdf',
            'contract'
        )

        result_list[0].convert('RGB').save(
            pdf_file_path,
            'PDF',
            resolution=100.0,
            save_all=True,
            append_images=[result.convert('RGB') for result in result_list[1:]]
        )

        img_save_path_list = []
        for result in result_list:
            img_file_path, img_save_path = file_middleware.get_save_path(
                '.png',
                'contract_img'
            )
            result.save(img_file_path)
            img_save_path_list.append(img_save_path)
        return pdf_save_path, img_save_path_list


image_process = ImageProcess()
