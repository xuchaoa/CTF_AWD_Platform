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

    class Meta:
        model = UserProfile
        fields = ['id']