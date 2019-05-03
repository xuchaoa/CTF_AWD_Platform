from django.shortcuts import render
from rest_framework import viewsets

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import viewsets,mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TeamSerializer,TeamAddSerializer
from .models import TeamProfile
from utils.permissions import IsAuthAndIsOwnerOrReadOnly
from django.db.models import Q
# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    '''
    团队操作:增删改查
    查：测试通过
    增加：
    '''
    # queryset = TeamProfile.objects.all()
    permission_classes = (IsAuthAndIsOwnerOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    # serializer_class = TeamSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'create':  #
            return TeamAddSerializer
        return TeamSerializer

    def get_queryset(self):
        return TeamProfile.objects.filter(Q(team_captain=self.request.user)|
                                          Q(team_member1=self.request.user)|
                                          Q(team_member2=self.request.user)|
                                          Q(team_member3=self.request.user))



