#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/15 下午 08:45

import xadmin
from . import models

class competition_display(object):
    '''显示的字段'''
    list_display = ['competition_name','competition_type','competition_choicenum']
    '''被检索的字段'''
    search_fields = ['competition_name']
    '''设置过滤选项'''
    list_filter = ['competition_name']
    '''每页显示条目数'''
    list_per_page = 10
    '''按id升序排列'''
    ordering = ['id']
    '''只读的字段'''
    readonly_fields = []
    '''被隐藏的字段(与只读矛盾)'''
    exclude = []

xadmin.site.register(models.CompetitionProfile, competition_display)