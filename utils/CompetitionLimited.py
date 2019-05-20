#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-19 下午8:20
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : CompetitionLimited.py
# @Software: PyCharm

from rest_framework import serializers
import datetime

def CompetitionIsStarted(competiton):
    start_time = competiton.competition_start
    end_time = competiton.competition_end
    now = datetime.datetime.now()
    if now < start_time:

        raise serializers.ValidationError({"402": "比赛未开始"})
    if now > end_time:
        raise  serializers.ValidationError({"403": "比赛已经结束"})
    else:
        pass

