from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import NoticeSerializer
from .models import NoticeProfile
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

class NoticeViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    公告ViewSet
    增加：不开放api
    删除：不开放api
    修改：不开放api
    查找：任何人（Auth）可以查看所有公告
    '''
    queryset = NoticeProfile.objects.all()
    serializer_class = NoticeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
