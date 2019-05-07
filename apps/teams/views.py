from django.shortcuts import render
from rest_framework import viewsets

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TeamDetailSerializer, TeamAddOrUpdateSerializer
from .models import TeamProfile
from utils.permissions import IsAuthAndIsOwnerOrReadOnly
from django.db.models import Q
from rest_framework import permissions
from info.models import TeamCompetitionInfo
from competition.models import CompetitionProfile


# Create your views here.

class TeamPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
        if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            '''
            只有队长可以修改
            '''
            return (obj.team_captain.id == request.user.id)
        if request.method == 'POST':
            '''
            任何auth的人都可以创建队伍
            '''
            return True

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True
        else:
            return False


class TeamViewSet(viewsets.ModelViewSet):
    '''
    团队操作:增删改查
    查：团队成员均可查看  --> 测试通过
    创建：任何人登陆的人 --> 测试通过
        自动在TeamCompetitionInfo中添加一条记录  --> ok
    修改：只有队长可以修改 --> ok
        修改是添加比赛操作：自动在TeamCompetitionInfo中添加一条记录  -->  ok
    删除：只有队长可以删除  --> ok
        删除队伍时删除相应记录  -->  ok
    '''
    # queryset = TeamProfile.objects.all()
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # serializer_class = TeamAddOrUpdateSerializer
    # lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'create':  #
            return TeamAddOrUpdateSerializer
        if self.action == 'update':
            return TeamAddOrUpdateSerializer
        return TeamDetailSerializer

    def get_permissions(self):
        # if self.action == 'update':
        #     return []

        # return [IsAuthAndIsOwnerOrReadOnly()]
        return [TeamPermission()]

    def get_queryset(self):
        return TeamProfile.objects.filter(Q(team_captain=self.request.user) |
                                          Q(team_member1=self.request.user) |
                                          Q(team_member2=self.request.user) |
                                          Q(team_member3=self.request.user))

    def perform_create(self, serializer):
        team = serializer.save()
        if team.competition is not None:
            TeamComInfo = TeamCompetitionInfo()
            TeamComInfo.team = team
            TeamComInfo.competition = team.competition
            TeamComInfo.save()

    def perform_update(self, serializer):
        team = serializer.save()
        if team.competition is not None:
            TeamComInfo = TeamCompetitionInfo()
            TeamComInfo.team = team
            TeamComInfo.competition = team.competition
            TeamComInfo.save()
    def perform_destroy(self, instance):
        competition = instance.competition
        TeamComInfo = TeamCompetitionInfo.objects.filter(Q(team=instance) & Q(competition=competition))
        TeamComInfo.delete()

        instance.delete()





