#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-18 上午9:05
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : test.py
# @Software: PyCharm

from celery_tasks.main import app
from utils.DEMO.SDK.CCPRestSDK import REST



import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CTF_AWD_Platform.settings")
django.setup()
from django.conf import settings
from django.core.mail import send_mail


@app.task()
def SendMail(code,recipient_list):

    message = '【SDUTCTF】 欢迎注册SDUTCTF平台，您的验证码为：{} ,验证码有效时间为五分钟。'.format(code)
    status = send_mail('注册SDUTCTF', '', settings.EMAIL_FROM, recipient_list, html_message=message)
    return status




@app.task()
def SendSMS(to,data,tempId):
    ACCOUNT_SID = '8a216da86a2a8174016a39f0748d09ec'
    AUTH_TOKEN = 'dd49474506d14a07b5acffdf0468c44f'
    serverIP='app.cloopen.com'
    serverPort='8883'
    softVersion='2013-12-26'
    appId = '8a216da86a2a8174016a39f074e809f3'

    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(ACCOUNT_SID, AUTH_TOKEN)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, data, tempId)
    return result
