from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group #引入model
from rest_framework import viewsets #引入viewsets，类似controllers
# from tutorial.quickstart.serializers import UserSerializer, GroupSerializer 官网模块引入写法，有误
from .serializers import UserSerializer, GroupSerializer #引入刚刚定义的序列化器

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined') #集合
    serializer_class = UserSerializer  #序列化

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
