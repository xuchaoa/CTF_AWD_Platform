from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import CompetitionSerializer
from .models import CompetitionProfile
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins

class CompetitionViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    比赛ViewSet
    增加：不开放api
    删除：不开放api
    修改：不开放api
    查找：任何人（Auth）可以查看全部比赛
    '''
    queryset = CompetitionProfile.objects.all()
    serializer_class = CompetitionSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
