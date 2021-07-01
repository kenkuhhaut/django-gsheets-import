from pathlib import Path



## Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

## SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dh(_h3&je&o*6r70xohamqbaro*2nx98qpuonw)a)wg4v*h@-!'

## SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



##
## Application definition
##

INSTALLED_APPS = [
    'literature.apps.LiteratureConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'import_export',
    'gsheets_import',
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

ROOT_URLCONF = 'urls'

TEMPLATES = [
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



##
## Database
##
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'literature.sqlite3',
    }
}



##
## Password validation
##
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



##
## Internationalization
##
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'CET'
USE_I18N = True
USE_L10N = True
USE_TZ = True



## Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

## Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



##
## Google Sheet import settings
##

## The Browser API key; see "Key" under "APIs & Services" > "Credentials" > "API Keys"
GSHEETS_IMPORT_API_KEY = '<API developers key>'

## The Client ID; see "Client ID" under "APIs & Services" > "Credentials" > "OAuth 2.0 Client IDs"
GSHEETS_IMPORT_CLIENT_ID = '<OAuth Client ID>'

## The App ID; see "Project Number" under "IAM & Admin" > "Settings"
GSHEETS_IMPORT_APP_ID = '<App ID>'
