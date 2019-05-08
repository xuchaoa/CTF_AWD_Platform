#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/16 上午 11:35

from .models import TeamProfile
import xadmin

class TeamDispaly(object):
    list_display = ('id','team_name','team_captain','team_member1','team_member2','team_member3','competition')

xadmin.site.register(TeamProfile, TeamDispaly)