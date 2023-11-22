## ERP管理系统-代码运行说明


## 开发环境要求
* Python版本为V3.9+
* Django版本为V3.2+
* Django-rest-framework版本为V3.12+
* Vue版本为2.6+
* 数据库为MySQL 8.0+
* 前端组件为AntD 1.x
* 其他Python包可参考requirements.txt文件


## 本地部署流程

### 前端部署

~~~
# 安装yarn
npm install yarn
# yarn安装依赖包
yarn install
# 前端 运行
yarn serve
# 前端 打包构建（打包前将utils/request.js里的baseurl按照注释指示的切换）
yarn build
~~~

### 后端部署

~~~
# 切换python环境
conda activate erp
# 安装依赖包
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
# 运行
python manage.py runserver
~~~

### 数据库部署

1. 数据库字符集设置为 utf8mb4
2. 创建 erp-db 数据库(先设置字符集, 再创建数据库)
    CREATE DATABASE erp_db;
3. 迁移数据库
    * python manage.py makemigrations
    * python manage.py migrate
4. 创建用户
    * python manage.py runscript create_user
5. 重置数据库
    * 导出erp_db数据库的结构
    * 删除数据库
    * 重新创建erp_db数据库
    * 执行上面的创建用户命令（编号请输入2，其他按照需求输入） python manage.py runscript create_user
    * 重新初始化权限 python manage.py runscript init_permission (去system_permission表里看一下，确保id从0开始)
    * 本地去打开menu.js最下面角色管理的注释，去页面里添加权限组

## 服务器部署流程

### 后端django部署
1. 配置 uwsgi
    pip install uwsgi
2. 运行 uwsgi
    uwsgi --ini [项目路径]/configs/uwsgi.ini

#### uwsgi配置文件
~~~
[uwsgi]
master = true
processes = 1
threads = 2
chdir = /www/wwwroot/erp.tanfuhua.com
wsgi-file= /www/wwwroot/erp.tanfuhua.com/project/wsgi.py
http = 0.0.0.0:8000
logto = /www/wwwroot/erp.tanfuhua.com/logs/error.log
chmod-socket = 660
vacuum = true
master = true
uid=root
gid=root
max-requests = 1000
~~~

### vue前端部署

1. 配置 nginx(配置文件在 /configs/nginx)
2. 构建前端文件
   进入 frontend 目录, yarn build
3. 将dist文件上传至服务器

#### nginx配置参数
~~~
server
{
    listen 80;
	listen 443 ssl http2;
    server_name 【域名地址】;
    root 【dist文件存放路径】;
    index  index.html index.htm;

    


    #SSL-START SSL相关配置，请勿删除或修改下一行带注释的404规则
    #error_page 404/404.html;
    ssl_certificate    /www/server/panel/vhost/cert/erp.tanfuhua.com/fullchain.pem;
    ssl_certificate_key    /www/server/panel/vhost/cert/erp.tanfuhua.com/privkey.pem;
    ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_ciphers EECDH+CHACHA20:EECDH+CHACHA20-draft:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    add_header Strict-Transport-Security "max-age=31536000";
    error_page 497  https://$host$request_uri;


    #SSL-END

    #ERROR-PAGE-START  错误页配置，可以注释、删除或修改
    #error_page 404 /404.html;
    #error_page 502 /502.html;
    #ERROR-PAGE-END

    #PHP-INFO-START  PHP引用配置，可以注释或修改
    include enable-php-73.conf;
    #PHP-INFO-END

    #REWRITE-START URL重写规则引用,修改后将导致面板设置的伪静态规则失效
    include /www/server/panel/vhost/rewrite/erp.tanfuhua.com.conf;
    #REWRITE-END

    #禁止访问的文件或目录
    location ~ ^/(\.user.ini|\.htaccess|\.git|\.svn|\.project|LICENSE|README.md)
    {
        return 404;
    }

    #一键申请SSL证书验证目录相关设置
    location ~ \.well-known{
        allow all;
    }

    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
    {
        expires      30d;
        error_log /dev/null;
        access_log /dev/null;
    }
    
  	location /api/ {
  		proxy_pass http://localhost:【后端运行端口地址】/api/;
  		proxy_set_header Host $http_host;
  		proxy_set_header X-Forwarded-Proto $scheme;
  	}

    location ~ .*\.(js|css)?$
    {
        expires      12h;
        error_log /dev/null;
        access_log /dev/null;
    }
    access_log  【日志文件存放地址】;
    error_log  【日志文件存放地址】;
}
~~~

### 数据库部署流程同本地部署流程一致
