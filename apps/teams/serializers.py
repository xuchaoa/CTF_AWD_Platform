#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/15 下午 02:18

from rest_framework import serializers
from .models import TeamProfile
from competition.serializers import CompetitionSerializer

class TeamDetailSerializer(serializers.ModelSerializer):
    '''
    增加5476
    '''

    competition = CompetitionSerializer()
    class Meta:
        model = TeamProfile
        fields = '__all__'

class TeamAddOrUpdateSerializer(serializers.ModelSerializer):
    '''
    用于增加用户
    '''
    team_captain = serializers.HiddenField(
        default=serializers.CurrentUserDefault
    )

    class Meta:

        model = TeamProfile
        fields = '__all__'