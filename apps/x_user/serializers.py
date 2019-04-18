#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/14 下午 09:18

from django.contrib.auth.models import User, Group #引入django身份验证机制User模块和Group模块
from rest_framework import serializers #引入rest framework的serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    '''
    UserInfo 类似于ModelForm
    '''
    class Meta:
        model = UserProfile
        # fields = ('id','user_name','user_school') #设置Api显示字段
        fields = '__all__'
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group  #使用Group model
#         fields = ('url', 'name')