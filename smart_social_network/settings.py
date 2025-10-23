import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env for all environments except production
if os.getenv('DJANGO_ENV') != 'production':
    load_dotenv()

# ========================
# Basic settings
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / 'apps'))
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-development-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

# List of allowed hosts
ALLOWED_HOSTS = ['*'] if DEBUG else [
    host.strip() for host in os.getenv('ALLOWED_HOSTS', '').split(',') if host.strip()
]


# ========================
# Application Definition
# ========================
INSTALLED_APPS = [
    # Other
    'daphne',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local applications
    'apps.users.apps.UsersConfig',
    'apps.admin_panel.apps.AdminPanelConfig',
    'apps.core.apps.CoreConfig',
    'apps.references.apps.ReferencesConfig',
    'apps.app_hub.apps.AppHubConfig',
    'apps.smart_password_manager.apps.SmartPasswordManagerConfig',
    'apps.auth_logs.apps.AuthLogsConfig',
    'apps.visits.apps.VisitsConfig',
    'apps.reports.apps.ReportsConfig',
    'apps.notices.apps.NoticesConfig',
    'apps.user_files.apps.UserFilesConfig',
    'apps.articles.apps.ArticlesConfig',
    'apps.friends.apps.FriendsConfig',
    'apps.user_images.apps.UserImagesConfig',
    'apps.posts.apps.PostsConfig',
    'apps.audio_files.apps.AudioFilesConfig',
    'apps.chats.apps.ChatsConfig',

    # Third-party applications
    'rest_framework',
    'tinymce',
    'debug_toolbar',
]

# ========================
#  Middleware
# ========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # Custom middleware
    'apps.admin_panel.middleware.AdminAccessMiddleware',
    'apps.users.middleware.user_activity.UpdateLastActivityMiddleware',
    # 'users.middleware.language.UserLanguageMiddleware',
]

ROOT_URLCONF = 'smart_social_network.urls'

# ========================
# Templates
# ========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_config',
                'apps.users.context_processors.user_context.user_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'smart_social_network.wsgi.application'


# ========================
# Database
# ========================
DB_ENGINE = 'django.db.backends.postgresql'
DB_NAME = os.getenv('DB_NAME', 'smart_social_network_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {
            'connect_timeout': 3 if DEBUG else 5,
            'options': '-c search_path=public' + (' -c statement_timeout=3000' if not DEBUG else ''),
            'sslmode': 'prefer' if DEBUG else 'require',
        },
        'CONN_MAX_AGE': 0 if DEBUG else 60,
        'DISABLE_SERVER_SIDE_CURSORS': False if DEBUG else True,
        'TEST': {
            'NAME': f"test_{DB_NAME}",
        },
    }
}

# Using SQLite for tests
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

# ========================
# Password validation
# ========================
AUTH_PASSWORD_VALIDATORS = [] if DEBUG else [
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


# ========================
# Authentication
# ========================
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = ''

# ========================
# Internationalization
# ========================
LANGUAGE_CODE = 'ru-ru' if DEBUG else 'en-us'
TIME_ZONE = 'Europe/Moscow' if DEBUG else 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
]

# ========================
# Static files
# ========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========================
#  REST Framework
# ========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer' if DEBUG else None,
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

# ========================
#  Celery
# ========================
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# ========================
# Caching
# ========================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "IGNORE_EXCEPTIONS": False,
        }
    },
    "sessions": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/2'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "IGNORE_EXCEPTIONS": True,
        },
        "TIMEOUT": 1209600,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "sessions"
SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_USE_SESSIONS = True


if not DEBUG:
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True

# ========================
#  TinyMCE
# ========================
TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'silver',
    'skin': 'oxide-dark',
    'plugins': '''
        advlist autolink lists link image charmap 
        searchreplace visualblocks code fullscreen
        table emoticons codesample help
        media preview insertdatetime quickbars
    ''',
    'toolbar': '''
        undo redo | formatselect | bold italic underline | 
        forecolor backcolor | alignleft aligncenter alignright |
        bullist numlist outdent indent | link image media |
        table codesample emoticons | code preview fullscreen help
    ''',
    'image_advtab': True,
    'quickbars_selection_toolbar': 'bold italic | quicklink h2 h3',
}

# ========================
# Security (production only)
# ========================
if not DEBUG:
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# =========================
ASGI_APPLICATION = 'smart_social_network.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

if DEBUG:
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]

DEBUG_TOOLBAR_ENABLED = os.getenv('DEBUG_TOOLBAR_ENABLED', 'True') == 'True'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG and DEBUG_TOOLBAR_ENABLED,
    'SQL_WARNING_THRESHOLD': 10,
    'PRETTIFY_SQL': True,
    'SHOW_COLLAPSED': True,
    'SQL_EXPLAIN': True,
}
