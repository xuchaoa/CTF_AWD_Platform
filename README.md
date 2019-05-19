## 概述
基于Django框架开发，同时kvm虚拟化和SDN技术的使用带给了使用者强大的靶机攻防体验。开发目的即一款优秀的专用于比赛的CTF平台，它丰富的比赛内容，灵活的比赛模式以及各项人性化的功能模块满足了比赛举办者的所有要求。然而，同时并不局限于比赛的用途，使用者同样可以用来练习CTF解题和靶机攻防。
## 技术栈

python3.7 + Django 2.1.7 + 10.3.9-MariaDB or Mysql-8.0 + REST Framework 3.9.2 + xadmin + Celery + Vue



## x
- superuser:admin@sdutctf123
- Django REST framework : admin@sdutctf123
- test ： test@sdutctf123

BeginTime: 2019.4.15 ~ now

## 安装说明
xadmin 

验证码模块：https://github.com/mbi/django-simple-captcha

dash: https://gitlab.com/k3oni/pydash-django-app/tree/master

## 临时解决方案（待讨论）
[已解决]无法修改User中基类中username字段的UNIQUE约束  -->>  注册时后台自动生成随机数进行填充
[已解决]重写django默认认证方法

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

## 安全问题

不得删除username的UNIQUE约束，否则会造成越权

## 测试

1. 注册验证码逻辑验证 -ok
2. 

## 附加工具
redis监控： http://www.treesoft.cn/dms.html

sentry: https://github.com/getsentry/sentry

