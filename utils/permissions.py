#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/5/3 下午 05:19
from rest_framework import permissions

class IsAuthAndIsOwnerOrReadOnly(permissions.BasePermission):
    '''
    需要登陆并且是所有者否则只能读取
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
        if request.method in permissions.SAFE_METHODS:  #SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
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