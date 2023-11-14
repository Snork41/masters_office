from pathlib import Path
import os
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'testserver',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'debug_toolbar',
    'mptt',
    'django_bootstrap5',
    'django_filters',
    'django_tables2',
    'about.apps.AboutConfig',
    'office.apps.OfficeConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'crispy_forms',
    'crispy_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'masters_office.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.year.year',
            ],
        },
    },
]
# DJANGO_TABLES2_TEMPLATE = os.path.join(BASE_DIR, 'templates/office/includes/table_employees.html')
EMPLOYEES_TABLE_TEMPLATE = os.path.join(BASE_DIR, 'templates/office/includes/table_employees.html')
POSTS_ORDER_TABLE_TEMPLATE = os.path.join(BASE_DIR, 'templates/office/includes/table_posts_order.html')


WSGI_APPLICATION = 'masters_office.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

TIME_ZONE = 'W-SU'

USE_I18N = True

USE_TZ = True


AUTH_USER_MODEL = 'users.CustomUser'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'office:index'
# LOGOUT_REDIRECT_URL = 'office:index'


# Восстановление паролей
if DEBUG:
    # Эмуляция почты
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
else:
    EMAIL_HOST = config("EMAIL_HOST", cast=str)
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    EMAIL_USE_TSL = config("EMAIL_USE_TSL", cast=bool)
    EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)

    EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", cast=str)


CSRF_FAILURE_VIEW = 'core.views.csrf_failure'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'action_formatter': {
            'format': '{levelname}: {asctime} {filename} "{message}"',
            'style': '{',
        },
        'request_formatter': {
            'format': '{levelname} {asctime} {module} {filename} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'action_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'encoding': 'utf-8',
            'maxBytes': 20000,
            'backupCount': 3,
            'delay': True,
            'filename': os.path.join(BASE_DIR, 'logs/action_file.log'),
            'formatter': 'action_formatter',
        },
        'request_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'encoding': 'utf-8',
            'maxBytes': 1000000,
            'backupCount': 2,
            'delay': True,
            'filename': os.path.join(BASE_DIR, 'logs/request_file.log'),
            'formatter': 'request_formatter',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'action_formatter',
        },
    },
    'loggers': {
        'office': {
            'handlers': ['action_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}


# Количество символов в тайтле поста
MAX_CHAR_TITLE = 15

# Разряд в должности
RANK = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]

# Работы по *** (в журнале ремонтных работ)
ORDER = [('Наряд', 'Наряд'), ('Распоряжение', 'Распоряжение')]

# Количество записей (пагинация) на страницах журнала:
AMOUNT_POSTS_WALK = 5  # обходов
AMOUNT_POSTS_REPAIR_WORK = 10  # ремонтных работ
AMOUNT_POSTS_ORDER = 10  # учета работ по нарядам и распоряжениям

# django-tables2 css
# Обшие настройки таблиц
DJANGO_TABLES2_TABLE_ATTRS = {
    'class': 'table table-hover',
    'thead': {
        'class': 'table-light sticky-top sticky-offset',
    },
}

# crispy_forms
# crispy_bootstrap5
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# django_filters
FILTERS_EMPTY_CHOICE_LABEL = 'Все'
