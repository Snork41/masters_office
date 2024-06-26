from pathlib import Path
import os
from decouple import config, Csv


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default='from_.env')

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    'about.apps.AboutConfig',
    'office.apps.OfficeConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',

    # 'debug_toolbar',
    'mptt',
    'django_bootstrap5',
    'django_filters',
    'django_tables2',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_ckeditor_5',
    'mailer',
    'simple_history',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
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
                'core.context_processors.notifications.check_new_resolutions',
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
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('MYSQL_DATABASE', default='django'),
        'USER': config('MYSQL_USER', default='django'),
        'PASSWORD': config('MYSQL_PASSWORD', default=''),
        'HOST': config('MYSQL_HOST', default=''),
        'PORT': config('MYSQL_PORT', default=3306, cast=int),
        'OPTIONS': {'charset': 'utf8mb4'},
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

TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


AUTH_USER_MODEL = 'users.CustomUser'


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'office:index'
LOGOUT_REDIRECT_URL = 'office:index'


# # Восстановление паролей
EMAIL_BACKEND = "mailer.backend.DbBackend"

EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TSL = config("EMAIL_USE_TSL", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)

EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", cast=str)
# # /Восстановление паролей


CSRF_FAILURE_VIEW = 'core.views.csrf_failure'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())

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
RANK = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7)
    ]

# Работы по *** (в журнале ремонтных работ)
ORDER = [
    ('Наряд', 'Наряд'),
    ('Распоряжение', 'Распоряжение')
]

# Количество записей (пагинация) на страницах журнала:
AMOUNT_POSTS_WALK = 5  # обходов
AMOUNT_POSTS_REPAIR_WORK = 10  # ремонтных работ
AMOUNT_POSTS_ORDER = 30  # учета работ по нарядам и распоряжениям


# django-tables2 css
# Обшие настройки таблиц
DJANGO_TABLES2_TABLE_ATTRS = {
    'class': 'table table-hover',
    'thead': {
        'class': 'table-light sticky-top sticky-offset',
    },
}
# Количество страниц в пагинаторе
DJANGO_TABLES2_PAGE_RANGE = 7

# crispy_forms
# crispy_bootstrap5
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# django_filters
FILTERS_EMPTY_CHOICE_LABEL = 'Все'


# ckeditor_5
customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]
        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

# from .local_settings import *
