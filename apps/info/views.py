from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .serializers import IllegalitySerializer, UserCompetitionInfoSerializer, TeamCompetitionInfoSerializer,CtfCompetitionTableSerializer, CtfSubmitAddSerializer, CtfSubmitDetailSerializer
from .models import TeamCompetitionInfo, UserCompetitionInfo, Illegality,CtfCompetitionTable, CtfSubmit, TeamCompetitionInfo
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.db.models import Q
from teams.models import TeamProfile



class TeamCompetitionInfoViewSet(viewsets.ModelViewSet):
    '''
    团队比赛总得分ViewSet
    增加：所有团队成员参赛可添加得分记录
    删除：不开放api
    更改：不开放api
    查询：任何人都可查看总得分
    '''
    queryset = TeamCompetitionInfo.objects.all()
    serializer_class = TeamCompetitionInfoSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


class UserCompetitionInfoViewSet(viewsets.ModelViewSet):
    '''
    团队比赛个人得分表ViewSet
    增加：所有人参加比赛可增加得分记录
    删除：不开放api
    修改：不开放api
    查询：所有人可查看得分记录
    '''
    queryset = UserCompetitionInfo.objects.all()
    serializer_class = UserCompetitionInfoSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


class IllegalityViewSet(viewsets.ModelViewSet):
    '''
    团队比赛违规表ViewSet
    增加：违规则增加记录
    删除：不开放api
    修改：不开放api
    查询：所有人可查询违规记录
    '''
    queryset = Illegality.objects.all()
    serializer_class = IllegalitySerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)




class CtfCompetitionTableViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    每场比赛ctf题目

    增加： None
    删除： None
    修改： None
    查看： 任何人（Auth）都可查看
    '''
    queryset = CtfCompetitionTable.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = CtfCompetitionTableSerializer


class CtfSubmitPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        '''
        删除、更改、Retrieve都会判断这里,增加记录时不会判断
        :param request:
        :param view:
        :param obj:
        :return:
        '''
        print(request)
        return False


class CtfSubmitViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    '''
    ctf提交记录

    增加： Auth并且参加了该比赛  ok
    并且在比赛时间内 TODO this
    修改相应表格： CtfCompetitionTable  ok   TeamCompetitionInfo
    删除： None
    修改： None
    查询： 只显示不敏感字段  --> ok
    '''
    queryset = CtfSubmit.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # serializer_class = CtfSubmitSerializer
    def get_serializer_class(self):
        if self.action == 'create':
            return CtfSubmitAddSerializer
        return CtfSubmitDetailSerializer

    def perform_create(self, serializer):
        submit = serializer.save()

        if submit.submit_result == True:
            team = TeamProfile.objects.get(
                Q(team_captain=submit.user) | Q(team_member1=submit.user) | Q(team_member2=submit.user)
                | Q(team_member3=submit.user))
            ctf_competition_table = CtfCompetitionTable.objects.get(
                Q(ctf=submit.ctf) & Q(competition=submit.competition))
            ctf_competition_table.submit_times += 1
            ctf_competition_table.save()
            team_competition_info = TeamCompetitionInfo.objects.get(Q(competition=submit.competition) & Q(team=team))
            team_competition_info.score_all += submit.ctf.ctf_score
            team_competition_info.score_ctf += submit.ctf.ctf_score
            team_competition_info.save()
        return submit

