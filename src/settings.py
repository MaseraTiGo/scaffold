# coding=UTF-8

"""
Django settings for project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys
import pymysql

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, SRC_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'interface',
    'abs.middleground.business.account',
    'abs.middleground.business.person',
    'abs.middleground.business.enterprise',
    'abs.middleground.business.transaction',
    'abs.middleground.business.production',
    'abs.middleground.business.merchandise',
    'abs.middleground.business.order',
    'abs.middleground.support.logistics',
    'abs.services.customer.account',
    'abs.services.customer.personal',
    'abs.services.customer.finance',
    'abs.services.crm.account',
    'abs.services.crm.staff',
    'abs.services.crm.tool'
]

MIDDLEWARE_CLASSES = [
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'


API_TEMPLATE_DIR = os.path.join(SRC_DIR, "interface/template")
FILE_TEMPLATE_DIR = os.path.join(SRC_DIR, "file/template")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [API_TEMPLATE_DIR, FILE_TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# MySQL数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    },
}

DATABASE_ROUTERS = ['src.database_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING = {
}

# Postgresql 数据库配置
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASS'),
#         'HOST': os.environ.get('DB_SERVICE'),
#         'PORT': os.environ.get('DB_PORT')
#     }
# }

REDIS_CONF = {
    'host': os.environ.get('REDIS_HOST'),
    'port': os.environ.get('REDIS_PORT'),
    'max_connections': os.environ.get('REDIS_POOL_SIZE'),
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/resource/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "resource"),
]

try:
    from logger_conf import *
except Exception as et:
    pass

try:
    from settings_local import *
except Exception as e:
    pass
