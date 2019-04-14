#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/14 下午 09:18

from django.contrib.auth.models import User, Group #引入django身份验证机制User模块和Group模块
from rest_framework import serializers #引入rest framework的serializers

class UserSerializer(serializers.HyperlinkedModelSerializer): #继承超链接模型解析器
    class Meta:
        model = User #使用User model
        fields = ('url', 'username', 'email', 'groups') #设置字段

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group  #使用Group model
        fields = ('url', 'name')