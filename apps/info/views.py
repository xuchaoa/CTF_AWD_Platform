from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import IllegalitySerializer, UserCompetitionInfoSerializer, TeamCompetitionInfoSerializer
from .models import TeamCompetitionInfo, UserCompetitionInfo, Illegality
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated


class TeamCompetitionInfoViewSet(viewsets.ModelViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
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


class UserCompetitionInfoViewSet(viewsets.ModelViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
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


class IllegalityViewSet(viewsets.ModelViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
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