# coding=UTF-8

import os

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "file"),
)

SECRET_KEY = 'n(ga_y0y4l&e8!tyt2)=f5q1=8(b=3&(cwvhfd*w8=0pm(0@00'

# Postgresql
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'crm',  # 数据库名字(需要先创建)
#         'USER': 'bq',  # 登录用户名
#         'PASSWORD': 'zxcde321BQ',  # 密码
#         # 'HOST': 'localhost',  # 数据库IP地址,留空默认为localhost
#         'HOST': 'localhost',  # 数据库IP地址,留空默认为localhost
#         'PORT': '5432',  # 端口
#     }
# }

# Postgresql数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crm_base',  # crm_201812282
        'USER': 'root',
        'PASSWORD': 'fsy007',
        'HOST': 'localhost',
        'PORT': '3306'
    },
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


REDIS_CONF = {
    'host': 'localhost',
    # 'host': 'localhost',
    # 'host': '192.168.3.250',
    'port': '6379',
    'max_connections': 500 ,
}

FILE_CONF = {
    'host': 'localhost',
    'port': '8001',
    'path': BASE_DIR + '/file/store/',
}

LOGGING = {
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
            'maxBytes': 1024 * 1024,
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
            'handlers': ['file', 'console'],
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
