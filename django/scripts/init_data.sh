#!/bin/bash

# Your initialization commands
echo "Running initialization tasks..."



#!/bin/bash
# 从第一行到最后一行分别表示：
# 1. 等待MySQL服务启动后再进行数据迁移。nc即netcat缩写
# 2. 收集静态文件到根目录static文件夹，
# 3. 生成数据库可执行文件，
# 4. 根据数据库可执行文件来修改数据库
# 5. 用 uwsgi启动 django 服务
# 6. tail空命令防止web容器执行脚本后退出
while ! nc -z db 3306 ; do
    echo "Waiting for the MySQL Server"
    sleep 3
done

python ./tools/rebuild_database.py
python manage.py runscript create_default_user
python manage.py runscript create_test_data

# Create a flag file to indicate initialization has been done
touch /app/initialized

exec "$@"

