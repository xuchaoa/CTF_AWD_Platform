#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/5/3 下午 07:48
from rest_framework import serializers
from .models import CompetitionProfile

class CompetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompetitionProfile
        fields = "__all__"