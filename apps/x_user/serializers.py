#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/14 下午 09:18

from django.contrib.auth.models import User, Group #引入django身份验证机制User模块和Group模块
from rest_framework import serializers #引入rest framework的serializers
from .models import UserProfile
from apps.x_team.models import TeamProfile


class TeamSerializer(serializers.ModelSerializer):  #嵌套外键序列化
    class Meta:
        model = TeamProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    '''
    UserInfo 类似于ModelForm
    '''
    user_team_id = TeamSerializer()
    class Meta:
        model = UserProfile
        # fields = ('id','user_name','user_school') #设置Api显示字段
        fields = '__all__'
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group  #使用Group model
#         fields = ('url', 'name')




class UserRegisterSerializer(serializers.ModelSerializer):
    '''
    注册S
    重写create方法
    '''
    def create(self, validated_data):
        user = super(UserRegisterSerializer,self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = UserProfile
        fields = '__all__'