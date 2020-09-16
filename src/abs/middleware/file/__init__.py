# coding=UTF-8

import os
import time
import random
# from wand.image import Image
from infrastructure.utils.common.single import Single
from infrastructure.core.exception.business_error import BusinessError
from settings import STATIC_URL, STATICFILES_DIRS
from abs.middleware.oss import OSSAPI


class FileMiddleware(Single):

    def get_save_file_name(self, name):
        names = name.split('.')
        name = "{}_{}.{}".format(
            str(random.randint(1000, 9999)),
            int(time.time()),
            names[-1]
        )
        return name

    def save_local(self, name, f_io, store_type = 'default'):
        new_name = self.get_save_file_name(name)
        base_dir = STATICFILES_DIRS[0]
        save_path = os.path.join(base_dir, store_type)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, new_name)
        with open(file_path, 'wb') as f:
            f.write(f_io.read())

        url = STATIC_URL + file_path.replace(base_dir, "")
        return url.replace("//", "/")


    def oss_store_type(self):
        return ["school", "major", "goods", "video", \
                "adsense", "person", "contract", \
                "agent", "idimg", "other", "contract/template"]

    def pdf_to_img(self):
        with Image(filename = 'https://orgdeer.oss-cn-hangzhou.aliyuncs.com/source/contract/contract/1004_1599479368.pdf') as img:
            with img.convert('jpeg') as converted:
                converted.save(filename = 'image.jpeg')

    def save_oss(self, name, f_io, store_type):
        '''
        self.pdf_to_img()
        '''
        if store_type not in self.oss_store_type():
            raise BusinessError("此上传分类不存在")
        new_name = "source/{}/{}".format(
            store_type,
            self.get_save_file_name(name)
        )
        imgurl = OSSAPI().put_object(new_name, f_io, "orgdeer")
        return imgurl

    def save(self, name, f_io, store_type, location = "local"):
        path = ""
        if location == "local":
            path = self.save_local(name, f_io)
        elif location == "oss":
            path = self.save_oss(name, f_io, store_type)

        return path


file_middleware = FileMiddleware()
