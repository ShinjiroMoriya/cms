import sys
import os
from datetime import timedelta
import urllib3
import dj_database_url
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

API_KEY = os.environ.get('API_KEY')
APPEND_SLASH = False
ALLOWED_HOSTS = [os.environ.get('HOST', '*')]
AUTH_CREDENTIALS = os.environ.get('AUTH_CREDENTIALS')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSRF_COOKIE_SECURE = True
DEBUG = os.environ.get('DEBUG', None) == 'True'
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
IP_ADDRESS = os.environ.get('IP_ADDRESS', '').split(',')
LANGUAGE_CODE = 'ja'
MAX_UPLOAD_SIZE = 5242880
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
ROOT_URLCONF = 'feed_app.urls'
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_AGE = timedelta(days=30).total_seconds()
SESSION_COOKIE_SECURE = True
SESSION_SAVE_EVERY_REQUEST = True
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = False
WSGI_APPLICATION = 'feed_app.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'category',
    'extra',
    'favorite',
    'group',
    'home',
    'introduction',
    'topic',
    'video',
]

if DEBUG:
    INTERNAL_IPS = ('127.0.0.1',)
    INSTALLED_APPS += [
        'sslserver',
        'debug_toolbar',
    ]

MIDDLEWARE = [
    'feed_app.caches_manager.CacheDatabaseUpdateMiddleware',
    'feed_app.api_limit.APILimitMiddleware',
    'feed_app.ip_limit.IpLimitMiddleware',
    'feed_app.basic_auth.BasicAuthMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'feed_app.minifyhtml.MinifyHTMLMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'feed_app.jinja2.environment',
        },
    },
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

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),
}

TEST_RUNNER = 'feed_app.test_runner.PostgresSchemaTestRunner'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.msgpack.MSGPackSerializer',
        },
        'TIMEOUT': 1 * 1 * 60 * 60,
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]

LOGGING = {
    'version': 1,
    'formatters': {
        'all': {
            'format': '\t'.join([
                '[%(levelname)s]',
                'code:%(lineno)s',
                'asctime:%(asctime)s',
                'module:%(module)s',
                'message:%(message)s',
            ])
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'all'
        },
    },
    'loggers': {
        'command': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
