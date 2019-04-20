#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/14 下午 09:56



from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path,re_path

# urlpatterns = [
#     # path('list/',views.UserListView.as_view()),
# ]

# router = DefaultRouter()
# router.register('user',views.UserListView)
#
# urlpatterns += router.urls