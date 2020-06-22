# coding=UTF-8

'''
Created on 2016年7月26日

@author: Administrator
'''

import sys
import os
from os.path import join

import unittest
import importlib

import init_envt


class UnitTest(object):

    def __init__(self, file_names):
        self._file_names = file_names
        self.base_dir = init_envt.BASE_DIR
        self._test_dir = join(join(self.base_dir, 'support'), 'test')

    def _load(self):
        module_names = []
        for root, dirs, files in os.walk(self._test_dir):
            for file in files:
                if file.startswith("test_") and file.endswith(".py") :

                    if self._file_names and not any(file_name in file for file_name in self._file_names):
                        continue

                    file_path = os.path.join(root,file)
                    file_path = os.path.splitext(file_path)[0]
                    module_name = file_path.replace(self.base_dir,"").replace(os.sep, '.')[1:]
                    module_names.append(module_name)

        modules = map(importlib.import_module, module_names)
        load = unittest.defaultTestLoader.loadTestsFromModule
        return unittest.TestSuite(map(load, modules))

    def run(self):
        test_suite = self._load()
        runner = unittest.TextTestRunner(verbosity = 2)
        runner.run(test_suite)

if __name__ == "__main__":
    test_file = [sys.argv[0]]
    file_names = sys.argv[1:]

    if len(file_names) > 0:
        UnitTest(file_names).run()
    else:
        print("Sorry, please input test file name.")
