from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .serializers import IllegalitySerializer, UserCompetitionInfoSerializer, TeamCompetitionInfoSerializer, \
    CtfCompetitionTableSerializer, CtfSubmitAddSerializer, CtfSubmitDetailSerializer, CompetitionChoiceDetailSerializer, \
    UserChoiceInfoAddSerializer,UserChoiceInfoUpdateSerializer,UserChoiceInfoDetailSerializer,CompetitionChoiceUpdateSerializer
from .models import TeamCompetitionInfo, UserCompetitionInfo, Illegality, CtfCompetitionTable, CtfSubmit, \
    TeamCompetitionInfo, CompetitionChoiceSubmit, UserChoiceInfo
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.db.models import Q
from teams.models import TeamProfile
import random
from choice.models import ChoiceLibrary
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.cache.mixins import cache_response
from .serializers import UserCompetitionInfoUpdateSerializer

from rest_framework import throttling


class Mythrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        return random.randint(1, 10) != 1


class TeamCompetitionInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    团队比赛总得分ViewSet
    增加：不开放api
    删除：不开放api
    更改：不开放api
    查询：任何人都可查看总得分
    权限控制：不能跨比赛访问 ok
    '''
    queryset = TeamCompetitionInfo.objects.all()
    serializer_class = TeamCompetitionInfoSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


class UserCompetitionInfoViewSet(mixins.UpdateModelMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    团队比赛个人得分表ViewSet
    增加：不开放api
    删除：不开放api
    修改：不开放api
    查询：所有人可查看得分记录
    '''
    queryset = UserCompetitionInfo.objects.all()
    # serializer_class = UserCompetitionInfoSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'update':
            return UserCompetitionInfoUpdateSerializer
        return UserCompetitionInfoSerializer


class IllegalityViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    团队比赛违规表ViewSet
    增加：不开放api
    删除：不开放api
    修改：不开放api
    查询：所有人可查询违规记录
    '''
    queryset = Illegality.objects.all()
    serializer_class = IllegalitySerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


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
        return False

from utils.IllegalityLimited import limited
from rest_framework.response import Response
from rest_framework import status
class CtfCompetitionTableViewSet(CacheResponseMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    每场比赛ctf题目

    增加： None
    删除： None
    修改： None
    查看： 任何人（Auth）都可查看
    权限控制： 只有该比赛用户可以查看(只能查看该比赛题目)  -->  ok
    '''
    queryset = CtfCompetitionTable.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = CtfCompetitionTableSerializer

    def get_queryset(self):

        team = TeamProfile.objects.filter(
            Q(team_captain=self.request.user) | Q(team_member1=self.request.user) | Q(
                team_member2=self.request.user) | Q(
                team_member3=self.request.user))
        team = team[0]
        competition = team.competition
        return CtfCompetitionTable.objects.filter(competition=competition)


class CtfSubmitViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    '''
    ctf提交记录

    增加： Auth并且参加了该比赛  ok
    并且在比赛时间内 ok
    修改相应表格： CtfCompetitionTable  ok   TeamCompetitionInfo  ok
    删除： None
    修改： None
    查询： 只显示不敏感字段  --> ok
    提交flag后不返回前端  -->  ok
    '''
    throttle_scope = 'CtfSubmit'

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # serializer_class = CtfSubmitSerializer

    def get_queryset(self):
        return CtfSubmit.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CtfSubmitAddSerializer
        return CtfSubmitDetailSerializer

    def get_real_score(self, score, times):
        '''
        定义降分策略
        :param score:
        :param times:
        :return:
        '''
        if times <= 3:
            return score
        else:
            lowest_score = score / 2
            _ = int((score - lowest_score) / 10)

            final_score = score - (times - 3) * _
            if final_score < lowest_score:
                final_score = lowest_score
            return final_score

    def perform_create(self, serializer):

        submit = serializer.save()

        if submit.submit_result == True:
            team = TeamProfile.objects.get(
                Q(team_captain=submit.user) | Q(team_member1=submit.user) | Q(team_member2=submit.user)
                | Q(team_member3=submit.user))
            ctf_competition_table = CtfCompetitionTable.objects.get(
                Q(ctf=submit.ctf) & Q(competition=submit.competition))
            times = ctf_competition_table.submit_times
            score = ctf_competition_table.ctf.ctf_score
            final_score = self.get_real_score(score=score, times=times)

            ctf_competition_table.submit_times += 1
            ctf_competition_table.save()

            team_competition_info = TeamCompetitionInfo.objects.get(Q(competition=submit.competition) & Q(team=team))
            team_competition_info.score_all += final_score
            team_competition_info.score_ctf += final_score
            team_competition_info.save()

            user_competition_info = UserCompetitionInfo.objects.get(Q(competition=submit.competition) & Q(team=team))
            user_competition_info.score_ctf += final_score
            user_competition_info.score_all += final_score
            user_competition_info.save()
        return submit


class CompetitionChoiceSubmitViewSet(mixins.ListModelMixin,  mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    '''
    比赛选择题Viewset
    增加：不开放API，自动生成
    删除：不开放API
    修改：注意敏感字段不允许修改
    查询：Auth 注意隐藏字段,只返回当前用户的选择题
    '''
    queryset = CompetitionChoiceSubmit.objects.all()
    permissions = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CompetitionChoiceDetailSerializer
        if self.action == 'update':
            return CompetitionChoiceUpdateSerializer
        return CompetitionChoiceDetailSerializer

    def get_queryset(self):
        return CompetitionChoiceSubmit.objects.filter(user=self.request.user)


class UserChoiceInfoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,mixins.UpdateModelMixin , viewsets.GenericViewSet):
    '''
    增加：判断是否已经有记录(unique约束实现)，更改状态(判断状态)，自动生成公户题库
    删除：不开放api
    修改：提交选择题时使用
    查询：Auth
    '''
    queryset = UserChoiceInfo.objects.all()
    permissions = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'create':
            return UserChoiceInfoAddSerializer
        elif self.action == 'update':
            return UserChoiceInfoUpdateSerializer
        elif self.action == 'list' or self.action == 'retrieve':
            return UserChoiceInfoDetailSerializer
        return UserChoiceInfoDetailSerializer

    def perform_create(self, serializer):
        # 生成题目操作  ok

        UserChoiceIn = serializer.save()
        competition = UserChoiceIn.competition
        team = UserChoiceIn.team
        user = UserChoiceIn.user
        choice_library = ChoiceLibrary.objects.all()
        choice_num = competition.competition_choicenum


        choice = random.sample(list(choice_library),choice_num)

        for i in choice:
            _ = CompetitionChoiceSubmit()
            _.competition = competition
            _.team = team
            _.user = user
            _.choice = i
            _.score = i.choice_score
            _.true_result = i.choice_answer
            _.save()


    def perform_update(self, serializer):
        # 判断题目并汇总分数   --  ok
        UserChoiceIn = serializer.instance
        competition = UserChoiceIn.competition
        team = UserChoiceIn.team
        user = UserChoiceIn.user
        choice_submit_queryset = CompetitionChoiceSubmit.objects.filter(competition=competition,team=team,user=user)
        score = 0
        for _ in choice_submit_queryset:
            if _.true_result == _.submit_result:
                _.result = True
                score += _.score
            else:
                _.result = False
            _.save()
        UserChoiceIn.score = score

        return serializer.save()
