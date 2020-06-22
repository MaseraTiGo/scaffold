# coding=UTF-8

'''
Created on 2016年8月6日

@author: Administrator
'''

# import python standard package

# import thread package

# import my project package
import os

init_dir = os.path.dirname((os.path.abspath(__file__)))
db_file_dir = os.path.join(init_dir,'db')


class FileManager(object):

    @classmethod
    def read_file(cls, file_name):
        abs_path = os.path.join(db_file_dir, file_name)
        line_list = []
        with open(abs_path,'rb') as f :
            for line in f.readlines():
                line = line.decode().strip()
                line_list.append(line)
        return line_list

