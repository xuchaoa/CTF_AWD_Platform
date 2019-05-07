#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/18 上午 08:09

import django_filters
from .models import UserProfile

class UserFilter(django_filters.rest_framework.FilterSet):
    '''
    None
    '''
    # def filter_queryset(self, request, queryset, view):
    #     if request.user.is_superuser:
    #         # print(True)
    #         return queryset
    #     else:
    #         return queryset.filter(username=request.user)

    id = django_filters.NumberFilter(field_name='id',lookup_expr='gte')
    username = django_filters.CharFilter(field_name='username',lookup_expr='icontains')  #模糊查询
    # 上后这个就跟search差不多了

    class Meta:
        model = UserProfile
        fields = ['id','username']