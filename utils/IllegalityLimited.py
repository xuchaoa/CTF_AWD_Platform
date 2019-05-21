#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-20 下午10:25
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : IllegalityLimited.py
# @Software: PyCharm


from rest_framework.response import Response
from rest_framework import status
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CTF_AWD_Platform.settings')
django.setup()
from info.models import Illegality
import datetime
from rest_framework import serializers


def limited(user=None):
    illegality = Illegality.objects.filter(user=user,duration_status=True).order_by("-illegality_endtime")

    if illegality is not None and illegality[0].duration_status:
        illegality = illegality[0]
        start_time = illegality.illegality_starttime
        end_time = illegality.illegality_endtime
        now = datetime.datetime.now()
        if now >= start_time and now <= end_time:
            raise serializers.ValidationError({"405": {"notice": "攻击比赛平台", "type": illegality.illegality_action,
                                                       "start_time": illegality.illegality_starttime,
                                                       "endtime": illegality.illegality_endtime,
                                                       'status': illegality.duration_status}})
        elif now > end_time:
            illegality.duration_status = False
            illegality.save()
        else:
            pass
