# foyer_babel/settings.py
<<<<<<< HEAD
from django.conf import settings
import os
from pathlib import Path


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jabloun.omaima5102000@gmail.com'
EMAIL_HOST_PASSWORD = '123456'  # Utilise un mot de passe d’application si 2FA activé
DEFAULT_FROM_EMAIL = 'Foyer Babel <jabloun.omaima5102000.com>'



AUTH_USER_MODEL = 'residents.Resident'
MEDIA_URL = '/media/'
LANGUAGE_CODE = 'fr-fr'
USE_I18N = True
USE_L10N = True

BASE_DIR = Path(__file__).resolve().parent.parent
# Static & Media Files
STATIC_URL = '/static/'
# settings.py
STATICFILES_DIRS = [
    BASE_DIR / 'residents' / 'static',
]

# Dossier pour collectstatic (en production)
STATIC_ROOT = BASE_DIR / 'staticfiles'

=======

import os
from pathlib import Path
MEDIA_URL = '/media/'


BASE_DIR = Path(__file__).resolve().parent.parent
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef

LOGIN_URL = 'login'  # Nom de l'URL
LOGIN_REDIRECT_URL = 'dashboard'  # Où aller après connexion
# settings.py

<<<<<<< HEAD
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


MEDIA_ROOT = str(BASE_DIR / 'media') 
=======
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef
# Security
SECRET_KEY = 'your-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

<<<<<<< HEAD



=======
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef
# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'residents',  # ✅ Your app
]

# Middleware & Templates
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foyer_babel.urls'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static & Media Files
STATIC_URL = '/static/'
<<<<<<< HEAD

MEDIA_URL = '/media/'
#MEDIA_ROOT = BASE_DIR / 'media'
=======
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
>>>>>>> e895eca4c3f584252cf6d671c0ac4c79addbddef

# Login
LOGIN_REDIRECT_URL = '/resident/dashboard/'
LOGIN_URL = '/login/'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'residents' / 'templates',  # Add this line to point to your templates
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