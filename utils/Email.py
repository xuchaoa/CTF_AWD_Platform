#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-13 上午10:46
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : Email.py
# @Software: PyCharm


import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CTF_AWD_Platform.settings")
django.setup()
from django.conf import settings
from django.core.mail import send_mail
from random import choice




def SendMail(code,recipient_list):

    message = '【SDUTCTF】 欢迎注册SDUTCTF平台，您的验证码为：{} ,验证码有效时间为五分钟。'.format(code)
    status = send_mail('注册SDUTCTF', '', settings.EMAIL_FROM, recipient_list, html_message=message)
    return status


# send_list = ['755563428@qq.com']
# SendMail(send_list)