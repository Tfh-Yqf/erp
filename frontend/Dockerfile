# 安装前端依赖
FROM registry.cn-hangzhou.aliyuncs.com/tfh/node:12.13.1
# 设置工作目录
WORKDIR /app
# 安装前端环境


CMD npm config set registry https://registry.npmmirror.com/ && \
        npm config set ignore-engines true && \
        npm install -g yarn && \
        yarn install && \
        yarn build