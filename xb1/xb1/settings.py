import os

from django.utils.translation import ugettext_lazy as _

#
#	DJANGO SETTINGS - DO NOT CHANGE
#	BEGIN
#

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'xb1.articles',
    'xb1.core',
    'xb1.contact',
    'xb1.forum',
    'xb1.eshop',
    'xb1.shop',
    'django_cleanup',
    'ckeditor',
    'ckeditor_uploader',
    'captcha',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xb1.urls'

BASE_DIR = os.path.realpath(os.path.dirname(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + "/templates/",
            BASE_DIR + "/articles/templates/",
            BASE_DIR + "/core/templates/",
            BASE_DIR + "/forum/templates/",
            BASE_DIR + "/eshop/templates/",
            BASE_DIR + "/shop/templates/",
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'xb1.core.context_processors.message_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'xb1.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


AUTH_USER_MODEL = "core.User"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"

LOGIN_URL = "login"
LOGOUT_URL = "logout"

PASSWORD_RESET_TIMEOUT = 1800

FORMAT_MODULE_PATH = [
    'formats',
]

LANGUAGES = (
    ('cs', _('Czech')),
    # ('en', _('English')),
)

LANGUAGE_CODE = 'cs'
TIME_ZONE = 'Europe/Prague'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

# CKEDITOR settings
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'article_content_images/'

CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Standard',
        'extraPlugins': 'autogrow',
        'width': '100%',
    },
    "comment": {
        'width': '100%',
        "toolbar": [["Bold", "Italic", "Underline", "SpellChecker"],],
    }
}
#
#	DJANGO SETTINGS
#	END
#


#
#	TEST SETTINGS - DO NOT CHANGE
#

WEB_DRIVER_LOCATION = BASE_DIR + '/resource/chromedriver'

#
#	ESHOP SETTINGS
#

ESHOP_BANK_ACCOUNT = "XXXXXXXX/YYYY"

#
#	EMAIL SETTINGS
#

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

EMAIL_HOST_USER = "xb1.feedback@gmail.com"
EMAIL_HOST_PASSWORD = 'fitwiki1'

FEEDBACK_EMAIL = "xb1.feedback@gmail.com"

#
#   SESSION SETTINGS
#
SESSION_COOKIE_AGE = 24 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True