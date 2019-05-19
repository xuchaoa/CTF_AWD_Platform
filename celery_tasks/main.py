#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-18 上午8:59
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : main.py
# @Software: PyCharm

from celery import Celery

# 为celery使用django配置文件进行设置，根据自己项目设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CTF_AWD_Platform.settings")

# 创建celery应用
app = Celery(main='celery_tasks')

# 导入celery配置
app.config_from_object('celery_tasks.config')

# 自动注册celery任务
app.autodiscover_tasks(['celery_tasks.SendCode'])

# app.start(argv=['celery', 'worker', '-l', 'info', '-f', 'logs/celery.log'])
# app.start(argv=['celery', 'worker', '-l', 'info', '-l', 'info'])