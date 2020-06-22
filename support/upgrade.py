# coding=UTF-8

'''
Created on 2016年7月26日

@author: Administrator
'''

import sys
import os
from os.path import join

import importlib
import init_envt

from support.upgrade.base import BaseUpgrade


class UpgradeHelper(object):

    def __init__(self, file_names):
        self._file_names = file_names
        self.base_dir = init_envt.BASE_DIR
        self._upgrade_dir = join(join(self.base_dir, 'support'), 'upgrade')

    def get_excutor(self, model):
        cls_set = set()
        for attr in dir(model):
            if(not attr.startswith("__")):
                obj = getattr(model, attr)
                if issubclass(obj, BaseUpgrade):
                    cls_set.add(obj)
        cls_set.remove(BaseUpgrade)
        return list(cls_set)

    def _load(self):
        module_names = []
        for root, dirs, files in os.walk(self._upgrade_dir):
            for file in files:
                if file.startswith("upgrade") and file.endswith(".py") :

                    if self._file_names and not any(file_name in file for file_name in self._file_names):
                        continue

                    file_path = os.path.join(root,file)
                    file_path = os.path.splitext(file_path)[0]
                    module_name = file_path.replace(self.base_dir,"").replace(os.sep, '.')[1:]
                    module_names.append(module_name)

        modules = map(importlib.import_module, module_names)
        excutors = []
        for module in modules:
            excutors.extend(self.get_excutor(module))
        return excutors

    def run(self):
        excutors  = self._load()
        for excutor in excutors:
            excutor().run()


if __name__ == "__main__":
    test_file = [sys.argv[0]]
    file_names = sys.argv[1:]

    if len(file_names) > 0:
        UpgradeHelper(file_names).run()
    else:
        print("Sorry, please input test file name.")
