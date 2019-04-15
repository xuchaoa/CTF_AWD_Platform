#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/15 上午 11:10

from xadmin import views
import xadmin

class GlobalSetting(object):
    # menu_style = 'accordion'  #分组折叠显示
    site_title = 'SDUTCtf'
    site_footer = 'ctf.sdutsec.cn'

xadmin.site.register(views.CommAdminView,GlobalSetting)  #注册到全局应用

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView,BaseSetting)
