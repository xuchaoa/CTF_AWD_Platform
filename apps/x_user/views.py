from django.shortcuts import render

# Create your views here.



from .serializers import UserSerializer
from .models import UserProfile
from rest_framework import mixins,generics
from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication  #基础验证。必须重写其中的方法
from rest_framework.permissions import IsAuthenticated,IsAdminUser  #直接调用
from rest_framework import permissions
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class MyAuth(BaseAuthentication):
    '''
    自定义认证
    '''
    def authenticate(self, request):
        pass
    def authenticate_header(self, request):
        pass


class IsOwnerOrReadOnly(permissions.BasePermission):  #无法细化=单条数据权限
    '''
    自定义权限
    '''
    message = 'this is a test msg'
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user

class UserFilter(filters.BaseFilterBackend):
    '''
    None
    '''
    def filter_queryset(self, request, queryset, view):
        print(type(request.user))
        if request.user.is_superuser:
            # print(True)
            return queryset
        else:
            return queryset.filter(username=request.user)


class UserProfilePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'



class UserProfileView(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    # pagination_class = UserProfilePagination   #TODO: some warinings
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (UserFilter,)
    # ordering = ('id',)
    ordering_fields = ('id',)
    filterset_fields = ('username','id')  #http://127.0.0.1:8000/api/user/?username=admin
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('=username','=id')  #搜索指定字段，支持多种搜索模式
    # filter_backends = (filters.OrderingFilter,)   #排序过滤
    # ordering_fields = ('username','id')




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









