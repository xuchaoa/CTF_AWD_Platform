from django.shortcuts import render

# Create your views here.


from .serializers import UserRegSerializer, SmsSerializer, UserDetailSerializer, LogSerializer, EmailSerializer
from .models import UserProfile, VerifyCode, UserLoginLog
from rest_framework import mixins, generics, permissions
from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication  # 基础验证。必须重写其中的方法
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # 直接调用
from .permissions import UserPermission
from .filters import UserFilter
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
# from .serializers import
from random import choice
from utils.SMS import SendSMS
from rest_framework import status
from rest_framework.response import Response
import platform
from user_agents import parse


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


from django.contrib.auth import get_user_model

User = get_user_model()  # 获取setting.py中AUTH_USER_MODEL指定的User model


class UserViewset(mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    User
    增加：
    删除：
    修改：
    查询：
    '''
    # queryset = UserProfile.objects.all()
    # serializer_class = UserRegSerializer
    pagination_class = UserProfilePagination  # fix warining #20
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # permission_classes = (UserPermission,)
    # lookup_field = 'id'  #自定义设置搜索哪个字段、在get_queryset之后过滤
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = UserFilter  # 自定义

    ordering_fields = ('id',)
    search_fields = ('=username', '=id')  # 搜索指定字段，支持多种搜索模式，默认模糊搜索

    def get_queryset(self):
        '''
        list: 只能显示当前用户信息
        # 如果有了这个那上面那句查询就不需要
        # 在这可以获取url后面的过滤然后进行一些操作
        # return UserProfile.objects.filter(id__gt=0)
        :return:
        '''
        return UserProfile.objects.filter(username=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return []
        elif self.action == 'update':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'update':  # 可能重置密码
            return UserRegSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    def get_object(self):
        '''
        Retrieve和Delete  会调用
        所有查询或者删除都是只返回当前用户，也就是基于当前用户。
        :return:
        '''
        return self.request.user


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成5位数字的验证码字符串
        """
        seeds = "1234567890"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        '''
        对CreateModelMixin 中的create方法进行重写，发送验证码并保存到数据库中
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = SendSMS()

        code = self.generate_code()
        data = [code, '5']  # 验证码在五分钟后失效

        sms_status = yun_pian.SendSms(to=mobile, data=data, tempId=1)
        print(sms_status)

        if sms_status["statusCode"] != '000000':
            return Response({
                "mobile": mobile
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile, type='mobile')
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


from utils.Email import SendMail


class EmailCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = EmailSerializer

    def generate_code(self):
        """
        生成5位数字的验证码字符串
        """
        seeds = "1234567890"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        list = []
        list.append(mobile)
        code = self.generate_code()
        send_status = SendMail(code, list)
        if send_status:
            code_record = VerifyCode(code=code, mobile=mobile, type='email')
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "mobile": mobile
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLogViewSet(viewsets.ModelViewSet):
    '''
    增加：不开放api
    删除：不开放api
    修改：不开放api
    查询：只能查询当前用户
    '''
    queryset = UserLoginLog.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LogSerializer

    def get_queryset(self):
        return UserLoginLog.objects.filter(user=self.request.user)


        # 获取OS
    def get_os(self, request):
        print("os---", platform.platform(request))
        return platform.platform(request)

    # 获取IP地址
    # def get_ip(request):
    #     try:
    #         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #         if x_forwarded_for:
    #             ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    #         else:
    #             ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    #     except:
    #         ip = None
    #
    #     # return HttpResponse("request_ip : %s" % ip)
    #     print("ip--",ip)
    #     return ip
    def get_ip(self, request):
        #if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        return ip

    #获取user-agent
    def get_ua(self, request):
        # return request.headers.get('User-Agent')
        ua_string = request.META.get('HTTP_USER_AGENT', '')
        # 解析为user_agent
        user_agent = parse(ua_string)
        # 判断浏览器
        bw = user_agent.browser.family
        # 判断操作系统
        s = user_agent.os.family
        # 输出
        print(ua_string)
        print(user_agent)
        print(bw)
        print(s)
        return bw

    def perform_create(self, serializer):
        UserLogin = UserLoginLog()
        # a = serializer.save()
        # print(a)
        UserLogin.user = self.request.user
        UserLogin.user_login_os = self.get_os(request=self.request)
        UserLogin.user_login_ip = self.get_ip(request=self.request)
        UserLogin.user_login_agent = self.get_ua(request=self.request)
        UserLogin.save()

# 下面是测试代码
#
#
# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Object-level permission to only allow owners of an object to edit it.
#     Assumes the model instance has an `owner` attribute.
#
#     """
#
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         # Instance must have an attribute named `owner`.
#         return obj.username == request.user
#
# from rest_framework import serializers
# class AddressSerializer(serializers.ModelSerializer):
#     '''
#     测试失败，因为username具有unique约束
#     '''
#     username = serializers.HiddenField(
#         default=serializers.CurrentUserDefault(),
#
#     )
#
#     class Meta:
#         model = User
#         fields = ("id", "username","user_phone")
#
#
# class PermissionTestViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
#     authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
#     serializer_class = AddressSerializer
#
#     def get_queryset(self):
#         return User.objects.filter(username=self.request.user)
