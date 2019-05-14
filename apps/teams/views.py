from django.shortcuts import render
from rest_framework import viewsets

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TeamDetailSerializer, TeamAddSerializer,TeamAddSerializer,JoinTeamSerializer
from .models import TeamProfile
from utils.permissions import IsAuthAndIsOwnerOrReadOnly
from django.db.models import Q
from rest_framework import permissions
from info.models import TeamCompetitionInfo,UserCompetitionInfo
from competition.models import CompetitionProfile
from rest_framework.response import Response
from rest_framework import status


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
            return TeamAddSerializer
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
        if hasattr(team,'competition') and team.competition is not None:
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



class JoinTeamViewSet(mixins.ListModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
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

    def perform_update(self, serializer):
        join_team = serializer.save()
        # team = TeamProfile.objects.get(team_token=join_team.team_token)
        if join_team.team_member1 is None:
            join_team.team_member1 = join_team.team_member
            join_team.save()
        elif join_team.team_member2 is None:
            join_team.team_member2 = join_team.team_member
            join_team.save()
        elif join_team.team_member3 is None:
            join_team.team_member3 = join_team.team_member
            join_team.save()
        else:
            serializer.x = 1


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        if serializer.x == 0:

            return Response(serializer.data)
        elif serializer.x == 1:
            return Response({
                "notice": "队伍已满"
            }, status=status.HTTP_400_BAD_REQUEST)






