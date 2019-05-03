#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/15 下午 02:18

from rest_framework import serializers
from .models import TeamProfile
from competition.serializers import CompetitionSerializer

class TeamSerializer(serializers.ModelSerializer):
    '''
    增加5476
    '''

    competition = CompetitionSerializer()
    class Meta:
        model = TeamProfile
        fields = '__all__'

class TeamAddSerializer(serializers.ModelSerializer):
    '''
    用于增加用户
    '''
    # team_captain = serializers.HiddenField(default=serializers.CurrentUserDefault)
    # def validate(self, attrs):
    #     attrs['team_captain'] = self.context['request'].user.id
    #     return attrs

    class Meta:
        model = TeamProfile
        fields = '__all__'