from django.shortcuts import render

# Create your views here.



from .serializers import UserSerializer
from .models import UserProfile
from rest_framework import mixins,generics
from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication  #基础验证。必须重写其中的方法
from rest_framework.permissions import IsAuthenticated,IsAdminUser  #直接调用
from .permissions import UserPermission
from .filters import UserFilter
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend



class MyAuth(BaseAuthentication):
    '''
    自定义认证
    '''
    def authenticate(self, request):
        pass
    def authenticate_header(self, request):
        pass







class UserProfilePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50



from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()  #获取setting.py中AUTH_USER_MODEL指定的User model

class UserCustomBackend(ModelBackend):
    '''
    自定义用户验证(全局配置就行)
    我们可以使用符号&或者|将多个Q()对象组合起来传递给filter()，exclude()，get()等函数。当多个Q()对象组合起来时，Django会自动生成一个新的Q()
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.object.get(Q(username=username) | Q(user_phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
#  上面验证加到全局中
# AUTHENTICATION_BACKENDS = (
#     'users.views.CustomBackend',
# )



class UserProfileView(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserProfilePagination   #   warining #20
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    permission_classes = (UserPermission,)


    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = UserFilter  #自定义

    ordering_fields = ('id',)
    search_fields = ('=username', '=id')  # 搜索指定字段，支持多种搜索模式
    # filterset_fields = ('username','id')  #http://127.0.0.1:8000/api/user/?username=admin

    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('=username','=id')  #搜索指定字段，支持多种搜索模式

    # filter_backends = (filters.OrderingFilter,)   #排序过滤
    # ordering_fields = ('username','id')


from .serializers import UserRegisterSerializer
class UserRegView(mixins.CreateModelMixin,viewsets.GenericViewSet):
    '''
    注册View
    '''
    queryset = UserProfile.objects.all()
    serializer_class = UserRegisterSerializer








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








