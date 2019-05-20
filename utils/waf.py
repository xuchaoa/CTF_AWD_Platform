#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-20 上午11:11
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : waf.py
# @Software: PyCharm

# print(self.request.META.get('HTTP_USER_AGENT', ''))
# print(self.request.data)
# print(self.request.query_params)

# 函数放置位置：get_queryset()  perform_create()

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CTF_AWD_Platform.settings')
django.setup()
from users.models import UserProfile
from teams.models import TeamProfile
from competition.models import CompetitionProfile
from django.db.models import Q
from info.models import Illegality
import time

ban_ua_0 = ['nmap','w3af','netsparker','nikto','fimap','acunetix','appscan','nessus','sqlmap']
ban_ua_1 = ['wget','python']
ban_ua_2 = []


def SetBan(user,duration,IllegalityAction):
    team = TeamProfile.objects.get(
        Q(team_captain=user) | Q(team_member1=user) | Q(team_member2=user) | Q(team_member3=user))
    competition = team.competition
    illegality = Illegality()
    illegality.user = user
    illegality.team = team
    illegality.competition = competition
    illegality.illegality_action = IllegalityAction
    illegality.illegality_duration = duration
    illegality.illegality_times += 1
    illegality.illegality_starttime = "2019-05-20 10:35:00.000000"
    illegality.illegality_endtime = "2019-05-20 10:35:00.000000"
    illegality.duration_status = True
    illegality.save()




def waf(user,query_params=None,data=None,ua=None):

    if ua is not None:
        for _ in ban_ua_0:
            if _ in ua:
                SetBan(user,20,1)
        for _ in ban_ua_1:
            if _ in ban_ua_1:
                pass
        for _ in ban_ua_2:
            if _ in ua:
                pass





if __name__ == '__main__':

    user = UserProfile.objects.get(id=1)
    waf(user=user,ua='sqlmap')
