from django.shortcuts import render

# Create your views here.



from .serializers import UserSerializer
from .models import UserProfile
from rest_framework import mixins,generics
from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication  #基础验证。必须重写其中的方法
from rest_framework.permissions import IsAuthenticated,IsAdminUser  #直接调用
from rest_framework import permissions

# Create your views here.

class MyAuth(BaseAuthentication):
    def authenticate(self, request):
        pass
    def authenticate_header(self, request):
        pass


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    自定义权限
    '''
    message = 'this is a test msg'
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user

class UserListView(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer





# from rest_framework.views import APIView
# from rest_framework.authentication import SessionAuthentication,BasicAuthentication
# from rest_framework.response import Response
# class TestView(APIView):
#     authentication_classes = (SessionAuthentication,BasicAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     def get(self,request,format=None):
#         content = 'testview'
#         return Response(content)





