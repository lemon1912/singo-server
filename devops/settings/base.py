__author__ = 'singo'
__datetime__ = '2019/4/3 1:59 PM '

"""
Django settings for devops project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
import datetime
import django.db.models.options as options
from pathlib import Path

# 自定义表权限位参数
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('is_purview',)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR =Path(__file__).parents[2]

# sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

ENV = os.getenv('devops_env', 'dev')


if ENV == 'test':
    DEBUG = True
    SECRET_KEY = 'cojnkm-8ukb)n(2btiud$rc+x-zl!to$$#_2nn&4p%89fle-lz'
    FRONT_END_URL = 'http://akama.test.ops.com'
elif ENV == 'pro':
    DEBUG = False
    SECRET_KEY = '=9p_gjl_d3*0-do^2%utnxqqp)i*yg5ma3z4&_el8m0v5!@x7r'
    FRONT_END_URL = 'http://akama.test.ops.com'
if ENV == 'dev':
    DEBUG = True
    SECRET_KEY = '%u6kxw-a4k-*87bd1)uu^9s-h141zq)o!a#kjval5s&^#$#q)#'
    FRONT_END_URL = 'http://127.0.0.1:9528'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '%u6kxw-a4k-*87bd1)uu^9s-h141zq)o!a#kjval5s&^#$#q)#'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 文档那边会调用admin用来登录
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'guardian',
    'django_apscheduler',
    'corsheaders',
    'django_filters',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'drf_yasg',
    'users.apps.UsersConfig',
    'resources.apps.ResourcesConfig',
    'saltManagement.apps.SaltManagementConfig',
    'workOrder.apps.WorkorderConfig',
    'purview.apps.PurviewConfig',
    'ldap.apps.LdapConfig',
    'SQLAudit.apps.SqlauditConfig',
    'deploy.apps.DeployConfig',
]

# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend', # 这是Django默认的
#     'guardian.backends.ObjectPermissionBackend', # 这是guardian的
# )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)


ROOT_URLCONF = 'devops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'devops.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  #设置了TIME_ZONE, 需要关闭USE_TZ, 否则会导致 DateTimeField 时间出错


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
        (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':
        (
        'rest_framework.permissions.IsAuthenticated',
        ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':10,
    # 'ORDERING_PARAM': "order",
    # 'SEARCH_PARAM': "search",
    # 'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S %z',
    # 'DATETIME_INPUT_FORMATS': ['%Y-%m-%d %H:%M:%S %z'],
    # 'DEFAULT_THROTTLE_CLASSES': (
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle'
    # ),
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '2/minute',
    #     'user': '3/minute'
    # }
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=14400), # 4 hours
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

EMAIL_HOST = 'smtp.189.cn'
EMAIL_PORT = 25
EMAIL_HOST_USER = '18058418418@189.cn'
EMAIL_HOST_PASSWORD ='Nj532680'
EMAIL_USE_TLS = True
EMAIL_FROM = EMAIL_HOST_USER

# LOGIN_REDIRECT_URL = '/users/v1/'
