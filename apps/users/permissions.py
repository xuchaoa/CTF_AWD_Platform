#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/19 上午 08:55

from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    '''
    自定义权限判断
    '''
    message = '您无权使用该请求或无权请求该资源'
    def has_object_permission(self, request, view, obj):
        '''
        object级别权限（后判断这个）  与这个设置相关联：mixins.RetrieveModelMixin
        :param request:
        :param view:
        :param obj:
        :return:
        '''
        return (obj.id == request.user.id)


    def has_permission(self, request, view):  ##bug fix
        '''
        model 级别权限（先判断这个）
        :param request:
        :param view:
        :return:  authenticated users return True
        '''
        if bool(request.user and request.user.is_authenticated):
            return True
        else:
            return False
