from pathlib import Path
import os


project_path = Path.cwd()

# 删除 migrations 文件
print('删除 migrations 文件')
for app in (project_path / 'apps').iterdir():
    if app.is_file() or not (app / 'migrations').exists():
        continue

    for file in (app / 'migrations').iterdir():
        if file.is_file() and file.name != '__init__.py':
            file.unlink()

# Python3 manage.py
print('构建数据库')
os.chdir(project_path)
os.system('python manage.py reset_db --noinput')
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

print('初始化权限')
os.system('python manage.py runscript init_permission')
