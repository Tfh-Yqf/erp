### 项目介绍
#### 开源的ERP系统，使用django+vue搭建，目前demo搭建在http://erp.tanfuhua.com上，有产品管理、采购管理、生成管理、销售管理、财务管理、报表统计、系统管理板块，包含不同权限，覆盖绝大部分ERP的场景（需要运行demo的可以留言一下我发你账号密码）

### 搭建运行环境

* pip install -r requirements.txt
* cd frontend  #进入frontend文件夹
* npm install -g @vue/cli  #安装vue脚手架
* npm install  #安装依赖包

### 本地运行

1. 启动后端服务
    python manage.py runserver
2. 启动前端服务
    npm run serve
3. 浏览器访问前端地址


### 界面截图
首页
![首页](img/shouye.png)
报表
![库存](https://gitee.com/himool/erp/raw/master/img/kucun.png)
产品
![产品](https://gitee.com/himool/erp/raw/master/img/%E4%BA%A7%E5%93%81.png)
采购
![采购](https://gitee.com/himool/erp/raw/master/img/%E9%87%87%E8%B4%AD.png)
销售
![销售](https://gitee.com/himool/erp/raw/master/img/%E9%94%80%E5%94%AE.png)
生产
![生产](https://gitee.com/himool/erp/raw/master/img/%E7%94%9F%E4%BA%A7.png)
库存
![库存](https://gitee.com/himool/erp/raw/master/img/%E5%BA%93%E5%AD%98.png)
财务
![财务](https://gitee.com/himool/erp/raw/master/img/%E8%B4%A2%E5%8A%A1.png)
设置
![设置](https://gitee.com/himool/erp/raw/master/img/%E8%AE%BE%E7%BD%AE.png)