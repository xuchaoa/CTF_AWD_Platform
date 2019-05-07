from rest_framework import serializers
from .models import Illegality, UserCompetitionInfo, TeamCompetitionInfo


class TeamCompetitionInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamCompetitionInfo
        fields = "__all__"


class UserCompetitionInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCompetitionInfo
        fields = "__all__"


class IllegalitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Illegality
        fields = "__all__"