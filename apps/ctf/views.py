from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import CtfSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import CtfLibrary

# Create your views here.

class CtfViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    增加：不提供前端API
    删除：不提供前端API
    修改：不提供前端API
    查找： 任何人（Auth）可以查看

    注意：在比赛没有开始之前无法查看  TODO this
    '''
    queryset = CtfLibrary.objects.all()
    serializer_class = CtfSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,JSONWebTokenAuthentication)


