#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-18 上午8:59
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : config.py
# @Software: PyCharm



BROKER_URL = "redis://:SDUTctf@10.6.65.231:6379/2"
# CELERY_BROKER_URL = "redis://:SDUTctf@10.6.65.231:6379/2"
CELERY_RESULT_BACKEND = 'redis://:SDUTctf@10.6.65.231:6379/3'

CELERY_ACCEPT_CONTENT = ['json']


# 设定 Celery 时区
CELERY_TIMEZONE = 'Asia/Shanghai'