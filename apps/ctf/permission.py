#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/18 上午 11:26

from rest_framework import permissions

class IpControl(permissions.BasePermission):
    '''
    ip黑名单访问控制，TODO: 基于用户的感觉更好,或者两者结合一下
    '''
    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        # blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
        # return not blacklisted
        return True

