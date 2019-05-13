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


class TeamDetailSerializer(serializers.ModelSerializer):
    '''
    查询使用
    '''

    competition = CompetitionSerializer()

    class Meta:
        model = TeamProfile
        fields = '__all__'


class CurrentUserIdDefault(serializers.CurrentUserDefault):
    def set_context(self, serializer_field):
        self.user_id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.user_id


class TeamAddOrUpdateSerializer(serializers.ModelSerializer):
    '''
    用于增加用户
    '''

    team_captain = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    team_name = serializers.CharField(max_length=100, validators=[UniqueValidator(queryset=TeamProfile.objects.all())])
    competition = serializers.PrimaryKeyRelatedField(required=True, queryset=CompetitionProfile.objects.all())
    team_token = serializers.CharField(max_length=30, read_only=True)

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
        attrs['team_token'] = token
        return attrs

    class Meta:
        model = TeamProfile
        fields = (
        "competition", "team_name", "team_token", "team_captain", "team_member1", "team_member2", "team_member3")
