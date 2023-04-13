import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-h+^pyp239f!mv7dw1=p+kp8cwvnr1koy&0&&=9+@xjiytl10)j'

# Add the custom authentication backend to the AUTHENTICATION_BACKENDS setting
AUTHENTICATION_BACKENDS = [
    'trading_bot.tradingbots.django.CustomModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'rest_framework.authentication.TokenAuthentication',
    # Other authentication backends...
]

# Set DEBUG to True to enable debugging during development, set to False in production
DEBUG = True

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',  # Set log level to DEBUG during development, INFO in production
    },
}

ALLOWED_HOSTS = ['playbotsnow.pythonanywhere.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'tradingbots.django',
    'django.contrib.contenttypes',    
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trading_bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tradingbots/django/templates/')],  # Add this line to include the templates folder path
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


WSGI_APPLICATION = 'trading_bot.wsgi.application'  # Updated to match your Django project name

# Rest of the settings.py file remains unchanged

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'super',
        'USER': 'Superuser',
        'PASSWORD': '@Mistle123',
        'HOST': 'playbotsnow-3124.postgres.pythonanywhere-services.com',
        'PORT': '13124',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = '/home/playbotsnow/trading_bot/media/'
STATIC_ROOT = '/home/playbotsnow/trading_bot/static/'

Please note that the SECRET_KEY and DEBUG settings should be updated based on your specific requirements and security considerations. Additionally, make sure to configure the logging settings according to your needs and disable DEBUG mode and adjust log levels accordingly when deploying your Django project to production for security reasons.
