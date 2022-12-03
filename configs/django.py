from pathlib import Path


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '8080',
        'PORT': '3306',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'NAME': 'erp',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
