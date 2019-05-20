#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/15 下午 02:18

from rest_framework import serializers
from .models import TeamProfile
from competition.serializers import CompetitionSerializer
from rest_framework.validators import UniqueValidator
from competition.models import CompetitionProfile
from random import choice
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response


class TeamDetailSerializer(serializers.ModelSerializer):
    '''
    查询使用
    '''

    competition = CompetitionSerializer()

    def validate(self, attrs):
        return attrs

    class Meta:
        model = TeamProfile
        fields = '__all__'


class CurrentUserIdDefault(serializers.CurrentUserDefault):


    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id


class TeamAddSerializer(serializers.ModelSerializer):
    '''
    用于删除用户
    '''

    team_captain = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    team_name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=TeamProfile.objects.all())])
    competition = serializers.PrimaryKeyRelatedField(required=True, queryset=CompetitionProfile.objects.all())
    team_token = serializers.CharField(max_length=30, read_only=True)

    def validate_team_captain(self,team_captain):
        existed = TeamProfile.objects.filter(Q(team_captain=team_captain) | Q(team_member1=team_captain) |
                                             Q(team_member2=team_captain) | Q(team_member3=team_captain))
        if existed:
            raise serializers.ValidationError('您已加入队伍，不能再创建队伍，请退出队伍后再试。')
        else:
            pass

    def generate_token(self):
        """
        生成30位随机字符串
        """
        seeds = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        random_str = []
        for i in range(30):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def validate(self, attrs):
        token = self.generate_token()
        attrs['team_captain'] = self.context['request'].user
        attrs['team_token'] = token
        return attrs

    class Meta:
        model = TeamProfile
        fields = ("competition", "team_name", "team_token", "team_captain","team_member1","team_member2","team_member3")


class JoinTeamSerializer(serializers.ModelSerializer):
    team_token = serializers.CharField(write_only=True,max_length=30,min_length=30,
                                       error_messages={
                                           'max_length':'token长度错误',
                                           'min_length':'token长度错误'
                                       })

    team_name = serializers.CharField(read_only=True)

    def validate_team_token(self, team_token):
        team = TeamProfile.objects.filter(team_token=team_token)
        if team is None:
            raise serializers.ValidationError('队伍token错误')
        else:
            pass
    def validate_team_member(self, team_member):
        existed = TeamProfile.objects.filter(Q(team_captain=team_member) | Q(team_member1=team_member) |
                                             Q(team_member2=team_member) | Q(team_member3=team_member))
        if existed:
            raise serializers.ValidationError('您已经加入其他队伍,请退出队伍后重试。')
        else:
            pass


    def validate(self, attrs):
        attrs['team_token'] = self.context['request'].data['team_token']
        attrs['team_member'] = self.context['request'].user
        return attrs

    class Meta:
        model = TeamProfile
        fields = ("id","team_name","team_token")


class QuitTeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    team_name = serializers.CharField(read_only=True)
    def validate_team_member(self, team_member):

        existed = TeamProfile.objects.filter(Q(team_captain=team_member) | Q(team_member1=team_member) |
                                             Q(team_member2=team_member) | Q(team_member3=team_member))
        if not existed:
            raise serializers.ValidationError('您未加入任何队伍')
        else:
            pass


    def validate(self, attrs):
        attrs['team_member'] = self.context['request'].user
        return attrs

    class Meta:
        model = TeamProfile
        fields = ("id","team_name")