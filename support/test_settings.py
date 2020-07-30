# coding=UTF-8

"""
Django settings for project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

try:
    from src.settings import *
    from src.settings_local import *
except Exception as e:
    pass

ALLOWED_HOSTS = ['*']
TEST_PORT = 8011
