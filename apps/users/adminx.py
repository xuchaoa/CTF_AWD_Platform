#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/15 上午 11:10

from xadmin import views
import xadmin
from . import models
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
# from xadmin import PermissionModelMultipleChoiceField
# from xadmin import Fieldset, Main, Side, Row
from xadmin.plugins.auth import UserAdmin
from django.utils.translation import ugettext as _


class GlobalSetting(object):
    # menu_style = 'accordion'  #分组折叠显示
    site_title = 'SDUTCtf'
    site_footer = 'ctf.sdutsec.cn'

xadmin.site.register(views.CommAdminView, GlobalSetting)  #注册到全局应用

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

class UserDisplay(UserAdmin):
    change_user_password_template = None
    list_display = ('user_phone','username', 'user_major', 'user_number',  'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'


    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = UserCreationForm
        else:
            self.form = UserChangeForm
        return super(UserDisplay, self).get_model_form(**kwargs)

    # def get_form_layout(self):
    #     if self.org_obj:
    #         self.form_layout = (
    #             Main(
    #                 Fieldset('',
    #                          'username', 'password',
    #                          css_class='unsort no_title'
    #                          ),
    #                 Fieldset(_('Personal info'),
    #                          Row('first_name', 'last_name'),
    #                          'email'
    #                          ),
    #                 Fieldset(_('Permissions'),
    #                          'groups', 'user_permissions'
    #                          ),
    #                 Fieldset(_('Important dates'),
    #                          'last_login', 'date_joined'
    #                          ),
    #             ),
    #             Side(
    #                 Fieldset(_('Status'),
    #                          'is_active', 'is_staff', 'is_superuser',
    #                          ),
    #             )
    #         )
    #     return super(UserDisplay, self).get_form_layout()

# xadmin.site.unregister(models.UserProfile)
xadmin.site.register(models.UserProfile, UserDisplay)


class VerifyCodeDisplay(object):
    list_display = ('id','code','mobile','add_time')

xadmin.site.register(models.VerifyCode, VerifyCodeDisplay)


