## 概述
基于Django框架开发，同时kvm虚拟化和SDN技术的使用带给了使用者强大的靶机攻防体验。开发目的即一款优秀的专用于比赛的CTF平台，它丰富的比赛内容，灵活的比赛模式以及各项人性化的功能模块满足了比赛举办者的所有要求。然而，同时并不局限于比赛的用途，使用者同样可以用来练习CTF解题和靶机攻防。
## 技术栈

Django 2.2 + 10.3.9-MariaDB + Celery + Vue

Restful 风格的 API 应该是前后端分离的最佳实践






## x
superuser:admin@ctf


## 安装说明
xadmin  windows下安装编码报错请直接使用如下
```
python -m pip install installed_module/xadmin-master.zip

```

### 修改兼容Django2.2如下：
http://www.cnblogs.com/xingfuggz/p/10142388.html


t = DEBUG_ENGINE.from_string(fh.read())
UnicodeDecodeError: 'gbk' codec can't decode byte 0xa6 in position 9737: illegal multibyte sequence