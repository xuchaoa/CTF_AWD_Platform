from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import CtfCompetitionTableSerializer, CtfSubmitAddSerializer, CtfSubmitDetailSerializer
from rest_framework import mixins
from .models import CtfCompetitionTable,CtfSubmit
from rest_framework import permissions
from django.db.models import Q


class TeamCompetitionInfoViewSet(viewsets.ModelViewSet):
    '''
    团队比赛总得分信息表

    增加：
    删除：
    更改：
    查询：
    '''
    pass


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


class CtfSubmitViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    ctf提交记录

    增加： Auth并且参加了该比赛  ok
    并且在比赛时间内 TODO this
    修改相应表格： CtfCompetitionTable        TeamCompetitionInfo
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
            ctf_competition_table = CtfCompetitionTable.objects.get(Q(ctf=submit.ctf) & Q(competition=submit.competition))
            ctf_competition_table.submit_times += 1
            ctf_competition_table.save()
        return submit

