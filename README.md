![](https://img.shields.io/badge/Version-1.0.0-green.svg)
![](https://img.shields.io/badge/License-MIT-blue.svg)
![](https://img.shields.io/badge/Author-SDUTSecLab-yellow.svg)


## 概述
基于Django框架开发，同时kvm虚拟化和SDN技术的使用带给了使用者强大的靶机攻防体验。开发目的即一款优秀的专用于比赛的CTF平台，它丰富的比赛内容，灵活的比赛模式以及各项人性化的功能模块满足了比赛举办者的所有要求。然而，同时并不局限于比赛的用途，使用者同样可以用来练习CTF解题和靶机攻防。
## 技术栈

python3.6 + Django 2.1.7 + 10.3.9-MariaDB or Mysql-8.0 + REST Framework 3.9.2 + xadmin + Celery + Vue

## 部署
基于ubuntu 18 LTS版本

安装mysql、redis 并在setting.py中配置连接信息

创建虚拟环境基于python3.6

安装requirements.txt中的依赖包,如果报下面的错误
```
OSError: mysql_config not found
```
```cmd
sudo apt-get install mysql-server mysql-client
```
然后mysql -V查看mysql是否安装成功
```cmd
sudo  apt-get install libmysqlclient-dev python3-dev
```

继续`pip install mysqlclient`就不会报错找不到'mysql_config'了

    
### docker install mysql 8.0 
```
docker pull mysql  #安装mysql 8.0
```
```
docker run -it --rm --name mysql -e MYSQL_ROOT_PASSWORD=SDUTctf123. -p 3306:3306 -d mysql 
```
进入容器
```
docker exec -it mysql bash 
```
新建ctf数据库
```
create database ctf;
```
### docker install redis
```
docker pull redis

docker run -d --name myredis -p 6379:6379 redis --requirepass "mypassword"  
  
python manage.py makemigrations

python manage.py migrate
```
### 创建管理员用户
```
python manage.py createsuperuser
```
### 运行celery异步任务
```cmd
celery -A celery_tasks.main  worker --loglevel=info
```
### 运行flower监控
```cmd
celery -A celery_tasks.main flower -l info --auto_refresh=True
```

## 其他安装说明（未整理）
xadmin 

验证码模块：https://github.com/mbi/django-simple-captcha

dash: https://gitlab.com/k3oni/pydash-django-app/tree/master

安全过滤初步想法：通过重载 SessionMiddleware 中间件来实现 或者自定义中间件

排行榜性能优化：signals实现缓存  或者 字段添加索引

邮箱验证注册功能

WP提交功能

## 注意事项

最后部署生产环境要更改 SECRET_KEY 

## 补充
DjangoCon 2008: Reusable Apps： https://www.youtube.com/watch?v=A-S0tqpPga4&feature=youtu.be

测试工具：coverage

API View: GenericAPIView

数据填充：Django  fixture

api验证： JWT  ： http://getblimp.github.io/django-rest-framework-jwt/

CORS实现：django-cors-headers

日志记录：logging


手机（邮箱）验证码方式进行登陆：

界面1： 手机号 验证码  用户名  密码

界面2： 跳转登陆界面后 -> 完善用户名、学号、班级、年级等信息


## 附加工具
redis监控： http://www.treesoft.cn/dms.html

sentry: https://github.com/getsentry/sentry




  

