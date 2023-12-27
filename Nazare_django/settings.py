import os
import environ
from django.urls import reverse


env = environ.Env()
environ.Env.read_env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG') == 'True'

ALLOWED_HOSTS = ['192.168.0.105', '127.0.0.1', '192.168.100.10',
                 '192.168.0.120', '192.168.0.121']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',
    'booking',
    'admin_reorder',
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

X_FRAME_OPTIONS = "SAMEORIGIN"

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
            ],
        },
    },
]

WSGI_APPLICATION = 'Nazare_django.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST"),
        'PORT': env("DATABASE_PORT"),
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

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'globalstatic')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ADMIN_REORDER = (
#     # Keep original label and models
#     'sites',
#
#     # Rename app
#     {'app': 'rm_app', 'label': 'Продукция',
#         'models': ('rm_app.ProductCategory', 'rm_app.ProductModel', 'rm_app.ProductChassis')},
#     {'app': 'rm_app', 'label': 'Производство',
#         'models': ('rm_app.Workshop', 'rm_app.Region', 'rm_app.WorkCenters', 'rm_app.AssemblyUnit')},
#     {'app': 'rm_app', 'label': 'Операции',
#      'models': ('rm_app.Operations',)},
#     {'app': 'pp_app', 'label': 'План производства',
#         'models': ('pp_app.MonthPlan',)},
#     {'app': 'hrd_app', 'label': 'Кадры', 'models': ('hrd_app.Worker',)},
#     {'app': 'wc_app', 'label': 'Рабочий процесс',
#         'models': ('wc_app.Interupts', 'wc_app.InteruptInWorkProcess', 'wc_app.WorkProcess')},
#     {'app': 'main_app', 'label': 'Пользователи', 'models': ('main_app.User',)}
# )
#
#
# AUTH_USER_MODEL = "main_app.User"
# LOGOUT_REDIRECT_URL = "/"
