FROM python:3.9
# 设置工作目录
WORKDIR /app
COPY .. /app
# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt install -y netcat-openbsd && apt install -y expect
# 设置 python 环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 暴露端口
EXPOSE 8000

# 移除\r in windows
RUN sed -i 's/\r//' ./start.sh
# 给start.sh可执行权限
RUN chmod +x ./start.sh
# 给start.sh可执行权限
RUN chmod +x ./scripts/init_data.sh
RUN chmod -R 777 ./logs/
CMD ["sh", "-c", "[ ! -f /app/initialized ] && /app/scripts/init_data.sh; /bin/bash ./start.sh"]
