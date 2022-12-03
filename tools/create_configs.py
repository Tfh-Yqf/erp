from pathlib import Path

BASE_DIR = Path.cwd()


def run():
    create_nginx_config()
    create_django_config()
    create_gunicorn_config()


def create_nginx_config():
    is_need_create = input('是否需要创建 Nginx 配置文件吗? (y/n)\n')
    if is_need_create == 'y':
        listen_port = input('请输入 Nginx 监听端口:\n')
        server_port = input('请输入 Django 启动端口:\n')
        static_path = BASE_DIR / 'frontend/dist/'

        with open('configs/nginx.conf', 'w') as file:
            file.write(f"""\
server {{
    listen {listen_port};
    charset utf-8;
    gzip_static on;

	location / {{
		root {static_path};
		index index.html index.html;
		try_files $uri $uri/ /index.html;
	}}

	location /api/ {{
		proxy_pass http://localhost:{server_port}/api/;
		proxy_set_header Host $http_host;
		proxy_set_header X-Forwarded-Proto $scheme;
	}}

	location /media/ {{
		proxy_pass http://localhost:{server_port}/media/;
		proxy_set_header Host $http_host;
		proxy_set_header X-Forwarded-Proto $scheme;
	}}
}}
""")


def create_django_config():
    is_production_environment = input('是否为生产环境? (y/n)\n')
    if is_production_environment == 'y':
        file_content = """\
from pathlib import Path


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

"""
    else:
        file_content = """\
from pathlib import Path


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

"""

    database_type = input('配置数据库: (sqlite: 0, mysql: 1)\n')
    if database_type == '1':
        host = input('请输入 host:\n')
        user = input('请输入 user:\n')
        passowrd = input('请输入 passowrd:\n')
        database_name = input('请输入 数据库名称:\n')

        file_content += f"""
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '{host}',
        'PORT': '3306',
        'USER': '{user}',
        'PASSWORD': '{passowrd}',
        'NAME': '{database_name}',
        'OPTIONS': {{'charset': 'utf8mb4'}},
    }}
}}
"""
    else:
        file_content += f"""
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}
"""
    with open(BASE_DIR / 'configs/django.py', 'w') as file:
        file.write(file_content)


def create_gunicorn_config():
    is_need_create = input('是否需要创建 Gunicorn 配置文件吗? (y/n)\n')
    if is_need_create == 'y':
        bind_address = input('请输入 Django 启动地址:\n')

        with open('configs/gunicorn.py', 'w') as file:
            file.write(f"""\
import multiprocessing


bind = '{bind_address}'
workers = multiprocessing.cpu_count() * 2 + 1
reload = True
daemon = True
""")


if __name__ == '__main__':
    run()
