"""
Django settings for datastore project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '_CHANGE_ME_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'datastore.apps.sra',
    'pipeline',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'datastore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'datastore', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'datastore.context_processors.google_analytics',
                'datastore.context_processors.idc_mirrors_version',
            ],
        },
    },
]

WSGI_APPLICATION = 'datastore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Caches
# https://docs.djangoproject.com/en/1.8/topics/cache/#cache-key-transformation
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = '/home/mirrors/static'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'datastore', 'static'),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

MEDIA_ROOT = '/home/mirrors/media'
MEDIA_URL = '/media/'

#####
#
# Google Analytics
#
#####
GOOGLE_ANALYTICS_PROPERTY_ID = os.environ.get('GOOGLE_ANALYTICS_PROPERTY_ID')


#####
#
# Logger config
#
#####
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s %(name)s.%(funcName)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'irods':{
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'datastore': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'sra': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

#####
#
# Pipeline config
#
#####
PIPELINE = {}
PIPELINE['COMPILERS'] = (
    'pipeline.compilers.sass.SASSCompiler',
)
PIPELINE_SASS_ARGUMENTS = '--update --compass --style compressed'

PIPELINE['CSS_COMPRESSOR'] = None
PIPELINE['JS_COMPRESSOR'] = None #'pipeline.compressors.slimit.SlimItCompressor'

# wildcards put the files in alphabetical order
# PIPELINE['STYLESHEETS']= {
#     'vendor': {
#         'source_filenames': (
#           'vendor/bootstrap-dist/css/bootstrap.css',
#           'vendor/bootstrap-datepicker/dist/css/bootstrap-datepicker3.css',
#         ),
#         'output_filename': 'css/vendor.css',
#     },
#     'main': {
#         'source_filenames': (
#           'css/main.css',
#           'css//global.css',
#         ),
#         'output_filename': 'css/main.css',
#     },
# }

# PIPELINE['JAVASCRIPT'] = {
#     'vendor': {
#         'source_filenames': (
#             'vendor/modernizer/modernizr.js',
#             'vendor/jquery/dist/jquery.js',
#             'vendor/bootstrap-ds/js/bootstrap.js',
#             'vendor/bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js',
#         ),
#         'output_filename': 'js/vendor.js',
#     },
# }


# compress when collect static
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
