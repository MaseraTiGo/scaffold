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
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR=os.path.join(BASE_DIR,"src")

sys.path.insert(0,BASE_DIR)
sys.path.insert(0,SRC_DIR)

ALLOWED_HOSTS=['*']
TEST_PORT=8000

# Application definition

INSTALLED_APPS=[
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'interface',
    'abs.middleground.business.account',
    'abs.middleground.business.person',
    'abs.middleground.business.enterprise',
    'abs.middleground.business.transaction',
    'abs.middleground.business.production',
    'abs.services.customer.account',
    'abs.services.customer.personal',
    'abs.services.customer.finance',
    'abs.services.crm.account',
    'abs.services.crm.staff',
]

MIDDLEWARE_CLASSES=[
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF='urls'


API_TEMPLATE_DIR=os.path.join(SRC_DIR,"interface/template")
FILE_TEMPLATE_DIR=os.path.join(SRC_DIR,"file/template")
TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [API_TEMPLATE_DIR,FILE_TEMPLATE_DIR],
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

WSGI_APPLICATION='wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE='en-us'

TIME_ZONE='Asia/Shanghai'

USE_I18N=True

USE_L10N=True

USE_TZ=False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL='/resource/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,"resource"),
]

DEBUG=True
SECRET_KEY='n(ga_y0y4l&e8!tyt2)=f5q1=8(b=3&(cwvhfd*w8=0pm(0@00'

# Postgresql数据库配置
DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'data',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'account': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'base_account',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'person': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'base_person',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'enterprise': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'base_enterprise',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'transaction': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'base_transaction',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'production': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'base_production',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'customer_account': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'customer_account',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'customer_personal': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'customer_personal',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'customer_finance': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'customer_finance',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'crm_account': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crm_account',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'crm_staff': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crm_staff',  # crm_201812282
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
    'crm_tool': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crm_tool',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

DATABASE_ROUTERS=['src.database_router.DatabaseAppsRouter']
DATABASE_APPS_MAPPING={
    'account': 'account',
    'person': 'person',
    'enterprise': 'enterprise',
    'transaction': 'transaction',
    'production': 'production',
    'customer_account': 'customer_account',
    'customer_personal': 'customer_personal',
    'customer_finance': 'customer_finance',
    'crm_account': 'crm_account',
    'crm_staff': 'crm_staff',
    'crm_tool': 'crm_tool'
}


# MySQL数据库配置
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'crm',
#         'USER': 'root',
#         'PASSWORD': 'zxcde321BQ',
#         # 'HOST': 'localhost',
#         'HOST': '192.168.3.250',
#         'PORT': '3306'
#     },
# }


REDIS_CONF={
    'host': 'localhost',
    # 'host': 'localhost',
    # 'host': '192.168.3.250',
    'port': '6379',
    'max_connections': 500,
}

LOGGING={
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024,
            'backupCount': 5,
            'filename': '/tmp/app/run.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django_docker': {
            'handlers': ['file','console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        }
    },
}
