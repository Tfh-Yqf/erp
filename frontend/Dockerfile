# 安装前端依赖
FROM node:12.13.1
# 设置工作目录
WORKDIR /app
COPY . /app
# 安装前端环境
RUN npm config set registry https://registry.npmmirror.com/
RUN npm config set ignore-engines true
RUN npm install -g yarn
RUN yarn install
RUN yarn build


