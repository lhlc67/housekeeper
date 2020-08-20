<p align="center"><img src="https://res.cloudinary.com/dtfbvvkyp/image/upload/v1566331377/laravel-logolockup-cmyk-red.svg" width="400"></p>


# 系统介绍

> 系统介绍网址 -> <http://39.106.160.132/index/>  

> 后台系统登录 -><http://39.106.160.132/lhlsite/laravel/public/admin/public/login>
> 账号：游客  密码：123456  

> 路由定义 /laravel/routes/web.php  

> 模型定义 /laravel/app/Admin  

> 控制器定义 /laravel/app/Http/Controllers/Admin

> 视图定义 /laravel/resources/views/admin  


## 软件部分目前完成功能

### RBAC鉴权授权机制

    通过 Manager,Role,Auth三张表实现以角色为中心的权限分配功能，经过超级管理员分配权限后，对应的角色只能访问相应的控制器下的方法这三张表的建表语句在laravel/database/migrations/目录下


### Echarts信息可视化

    单片机直接与阿里云ESC上的MYSQL数据库进行连接，连接成功后每小时  向数据库发送当时采集到的温度、湿度等环境信息，MYSQL接受到信息后将数据存入数据库。
    实时数据直接通过HTTP请求发送到Laravel(开放出  不需要CSRF验证的路由)保存至缓存中前端用Echarts分别展示实时数据和  历史数据

### 邮件信息订阅

    如果实时数据超过某一预定阈值，Laravel通过绑定的邮箱STMP服务器来给预定该服务的Manager发送邮件

## Web框架 Laravel



- [简单，快速的路由引擎]().
- [强大的依赖项注入容器]().
-[ 富有表现力，直观的数据库ORM]().
- [与数据库无关的模式迁移]().
- [强大的后台工作处理]().
- [实时事件广播]().

## 软件子系统 
云端开发环境搭建云端操作系统选择Ubuntu sever，进行基本配置后部署开发环境，首先安装Nginx配置负载均衡、MySQL开放远程连接许可给树莓派。然后部署PHP的Web框架Laravel，小程序的接口也由它提供，系统的静态资源文件存入阿里云对象存储OSS内。

## 软件系统与硬件系统的交互
    树莓派将婴儿睡眠视频传入阿里云OSS对象存储内，同时将视频信息存入云端数据库中，云端会在网站和微信小程序上展示睡眠视频。同时婴儿睡眠环境信息比如温湿度等会通过HTTP协议实时发送到阿里云搭建的后端，用户可以在网站上以Echarts可视化图标的形式查看环境信息。








