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
        print(obj)
        print(dir(obj))
        print('ssss')
        print(request.user.id)
        if bool(request.user and request.user.is_authenticated):
            print('1')
            if request.method in ('GET', 'HEAD', 'OPTIONS','PUT'):
                return (obj.id == request.user.id)
            elif request.user.is_superuser:
                return True
            else:
                return False
        else:
            return False

    def has_permission(self, request, view):  ##TODO 权限控制 bug
        '''
        model 级别权限（先判断这个）
        :param request:
        :param view:
        :return:
        '''
        if bool(request.user and request.user.is_authenticated):
            return True
        else:
            return False