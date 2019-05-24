from django.shortcuts import render
from rest_framework import viewsets

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TeamDetailSerializer, TeamAddSerializer, TeamAddSerializer, JoinTeamSerializer, QuitTeamSerializer
from .models import TeamProfile
from utils.permissions import IsAuthAndIsOwnerOrReadOnly
from django.db.models import Q
from rest_framework import permissions
from info.models import TeamCompetitionInfo, UserCompetitionInfo
from competition.models import CompetitionProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .serializers import TeamUpdateserializer

# Create your views here.

class TeamPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
        if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            '''
            只有队长可以删除修改
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
        自动在UserCompetitionInfo中添加一条记录  --> ok
    修改：只有队长可以修改 --> ok
        修改是添加比赛操作：自动在TeamCompetitionInfo中添加一条记录  -->  ok
    删除：只有队长可以删除  --> ok
        删除队伍时删除相应记录  -->  ok --> 数据库CASCADE实现
    '''

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # serializer_class = TeamAddOrUpdateSerializer
    # lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'create':  #
            return TeamAddSerializer
            # return TeamAddSerializer
        if self.action == 'update':
            return TeamUpdateserializer
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
        if hasattr(team, 'competition') and team.competition is not None:
            TeamComInfo = TeamCompetitionInfo()
            TeamComInfo.team = team
            TeamComInfo.competition = team.competition
            TeamComInfo.save()
            UserComInfo = UserCompetitionInfo()
            UserComInfo.team = team
            UserComInfo.user = team.team_captain
            UserComInfo.competition = team.competition
            UserComInfo.save()

    def perform_update(self, serializer):
        '''
        只允许用来删除队员,添加队员未限制
        注意一次只能删除一个队员
        :param serializer:
        :return:
        '''
        team = serializer.instance
        # after_team = serializer.initial_data
        after_team = serializer.validated_data
        if team.team_member1 is not None and after_team['team_member1'] is None:
            user_competition_info = UserCompetitionInfo.objects.filter(user=team.team_member1)
        elif team.team_member2 is not None and after_team['team_member2'] is None:
            user_competition_info = UserCompetitionInfo.objects.filter(user=team.team_member2)
        elif team.team_member3 is not None and after_team['team_member3'] is None:
            user_competition_info = UserCompetitionInfo.objects.filter(user=team.team_member3)
        print(user_competition_info[0])
        print(1)
        return serializer.save()

    def perform_destroy(self, instance):
        competition = instance.competition
        TeamComInfo = TeamCompetitionInfo.objects.filter(Q(team=instance) & Q(competition=competition))
        TeamComInfo.delete()

        instance.delete()


class JoinTeamViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    '''
    增加：
    删除：
    修改： 只要有token就可以加入队伍
    查询：
    '''
    queryset = TeamProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = JoinTeamSerializer
    flag = 0

    def perform_create(self, serializer):

        team = serializer.validated_data

        join_team = TeamProfile.objects.get(team_token=team['team_token'])
        if join_team.team_member1 is None:
            join_team.team_member1 = team['team_member']
            join_team.save()
        elif join_team.team_member2 is None:
            join_team.team_member2 = team['team_member']
            join_team.save()
        elif join_team.team_member3 is None:
            join_team.team_member3 = team['team_member']
            join_team.save()
        else:
            self.flag = 1
        # serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if self.flag == 0:

            return Response({
                "notice":"加入队伍成功"
            },status=status.HTTP_200_OK)
        elif self.flag == 1:
            return Response({
                "notice": "队伍已满"
            }, status=status.HTTP_400_BAD_REQUEST)


class QuitTeamViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin ,viewsets.GenericViewSet):
    '''
    增加：
    删除：
    修改： 用户退出当前队伍
    查询：
    '''
    queryset = TeamProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = QuitTeamSerializer

    def perform_create(self, serializer):
        quit_team = serializer.validated_data
        member1 = TeamProfile.objects.filter(team_member1=quit_team['team_member'])
        member2 = TeamProfile.objects.filter(team_member2=quit_team['team_member'])
        member3 = TeamProfile.objects.filter(team_member3=quit_team['team_member'])

        if not member1 and not member2 and not member3:
            raise serializers.ValidationError("您未加入任何队伍")
        elif member1 :
            member1[0].team_member1 = None
            member1[0].save()
        elif member2 :
            member2[0].team_member2 = None
            member2[0].save()
        elif member3 :
            member3[0].team_member3 = None
            member3[0].save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)


