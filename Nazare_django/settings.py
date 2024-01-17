import os
from datetime import datetime, timezone

import environ
from django.urls import reverse


env = environ.Env()
environ.Env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG') == 'True'

ALLOWED_HOSTS = ['192.168.0.105', '127.0.0.1', '192.168.100.10',
                 '192.168.0.120', '192.168.0.121']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_reorder',
    'index.apps.IndexConfig',
    'booking',
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'Nazare_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.common_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'Nazare_django.wsgi.application'


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'sql_mode': 'traditional',
            },
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/index/static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'globalstatic')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


ADMIN_REORDER = (
    {'app': 'index', 'label': 'Апартаменты',
        'models': ('index.Apartment',)},
    {'app': 'index', 'label': 'Меню',
        'models': ('index.Category', 'index.SubCategory', 'index.RedirectPage',)},
    {'app': 'index', 'label': 'Контактные данные',
        'models': ('index.ContactPage',)},
    {'app': 'booking', 'label': 'Бронирование',
        'models': ('booking.Booking', 'booking.Guest',)}
)


EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL') == 'True'
