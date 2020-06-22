# coding=UTF-8

import os


class FileHelper(object):

    @staticmethod
    def write_file():
        pass

    @staticmethod
    def del_file(path):
        if os.path.exists(path):
            os.remove(path)
        return True

    @staticmethod
    def mv_file():
        pass

    @staticmethod
    def cp_file():
        pass

    @staticmethod
    def __recursive_mk_path(path, sep = '\\' , is_file = False):
        path_list = path.split(sep)
        for index in range(1, len(path_list), 1):
            sub_path_list = path_list[0:index + 1]
            sub_path = sep.join(sub_path_list)
            if not os.path.exists(sub_path):
                if not is_file:
                    os.mkdir(sub_path)
                else:
                    pass # 是文件的 暂不考虑
        return True

    @classmethod
    def mk_dir(cls, dir_path):
        if not os.path.exists(dir_path):
            cls.__recursive_mk_path(dir_path)

    @classmethod
    def mk_dirs(cls, dir_paths):
        for dir_path in dir_paths:
            cls.mk_dir(dir_path)

if __name__ == "__main__":
    t = r"D:\ztcjingling\ebus\analysis\test"
    FileHelper.mk_dir(t)
