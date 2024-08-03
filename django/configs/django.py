from pathlib import Path


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'db',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'ERPSYSTE',
        'NAME': 'erp_db',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
