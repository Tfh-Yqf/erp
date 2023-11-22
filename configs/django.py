from pathlib import Path


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'your database Ip Or Domain',
        'PORT': 'your_port',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'NAME': 'erp_db',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
