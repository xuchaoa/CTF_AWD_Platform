#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/15 下午 02:18

from rest_framework import serializers
from .models import TeamProfile
from competition.serializers import CompetitionSerializer

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
    # team_captain = serializers.PrimaryKeyRelatedField(
    #     default=serializers.CurrentUserDefault(),read_only=True
    # )

    class Meta:

        model = TeamProfile
        fields = '__all__'