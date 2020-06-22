# coding=UTF-8

'''
Created on 2016年7月26日

@author: Administrator
'''

import sys
import os
import django

from os.path import abspath, dirname, join

BASE_DIR = dirname(dirname(abspath(__file__)))
SRC_DIR = join(BASE_DIR, "src")

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, SRC_DIR)

try:
    import settings  # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

os.environ.update({"DJANGO_SETTINGS_MODULE": "settings"})
django.setup()
