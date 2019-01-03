# DailyFresh
>通过Docker部署Django应用(MySQL/Redis/Celery...)
>实现一个电商网络平台,利用docker搭建分布式架构,最终实现一键部署

## 安装Docker
https://www.docker.com/get-started
下载对应Linux.Mac或者Win平台的Docker

## 克隆项目到本地

打开本地终端,执行:
>clone https://github.com/Rousong/DailyFresh

## 运行项目
**运行docker**

然后在项目目录内打开终端执行:
>docker-compose up

稍微等待片刻等待命令执行完毕...

通过 `127.0.0.1:8000`即可访问项目 

## 运行flower（队列任务监视后台）
>通过docker exec -i -t dailyfresh_web_1 bin/bash

**进入容器内部**
>执行 flower --broker=redis://redis:6379/1 即可


## 设置远程登录docker内部mysql数据库
>通过 docker exec -i -t dailyfresh_db_1 bin/bash
进入数据库docker内

>输入 mysql -uroot -p 进去mysql命令行模式

创建一个mysql用户,并设置可以远程访问
>grant usage on *.* to 'testuser'@'localhost' identified by 'testpassword';//创建用户fred密码ferd

>select host,user,password from mysql.user where user='fred';//查看记录  

>grant all privileges on *.* to fred@'%'identified by 'fred';//设置可以远程访问

>flush privileges;//刷新权限
