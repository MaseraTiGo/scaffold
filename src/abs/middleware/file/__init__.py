# coding=UTF-8

import os
import time
from infrastructure.utils.common.single import Single
from settings import FILE_CONF


class FileMiddleware(Single):

    def get_save_file_name(self, name):
        names = name.split('.')
        name = "{}_{}.{}".format(names[0], int(time.time()), names[-1])
        return name

    def save(self, name, f_io, store_type = 'default'):
        new_name = self.get_save_file_name(name)
        save_path = os.path.join(FILE_CONF['path'], store_type)
        if not os.path.exists(save_path):
            print(save_path)
            os.makedirs(save_path)
        file_path = os.path.join(save_path, new_name)
        with open(file_path, 'wb') as f:
            f.write(f_io.read())
        return file_path


file_middleware = FileMiddleware()
