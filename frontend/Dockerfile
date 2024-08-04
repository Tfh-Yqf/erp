# 安装前端依赖
FROM node:12.13.1
# 设置工作目录
WORKDIR /app

# 安装前端环境
CMD npm config set registry https://registry.npmmirror.com/
CMD npm config set ignore-engines true
CMD npm install -g yarn
CMD ["yarn","install"]
CMD ["yarn","build"]