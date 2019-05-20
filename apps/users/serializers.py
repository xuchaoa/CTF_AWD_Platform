#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/14 下午 09:18

from django.contrib.auth.models import User, Group  # 引入django身份验证机制User模块和Group模块
from rest_framework import serializers  # 引入rest framework的serializers
from .models import UserProfile
from teams.models import TeamProfile
import re
from datetime import datetime
from .models import VerifyCode, UserLoginLog
from datetime import timedelta
from CTF_AWD_Platform.settings import REGEX_MOBILE, REGEX_EMAIL
from rest_framework.validators import UniqueValidator  # 直接调用封装好的

from django.contrib.auth import get_user_model

User = get_user_model()


class TeamSerializer(serializers.ModelSerializer):  # 嵌套外键序列化
    class Meta:
        model = TeamProfile
        fields = '__all__'


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册序列化
    '''
    # user_team_id = TeamSerializer()  #暂时无用
    '''
    write_only=True  设置这个属性为true,去确保create/update的时候这个字段被用到，序列化的时候，不被用到,也就是不会被返回
    '''
    code = serializers.CharField(required=True, max_length=6, min_length=6,
                                 error_messages={
                                     "blank": "字段Value为空",
                                     "required": "无字段Key",
                                     "max_length": "验证码长度错误",
                                     "min_length": "验证码长度错误"
                                 },
                                 write_only=True, help_text='验证码')  # write_only=True只写入，不会在创建成功后返回
    user_phone = serializers.CharField(help_text="用户名", allow_blank=False,
                                       validators=[UniqueValidator(queryset=User.objects.all(), message="手机号已经存在")])

    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    password = serializers.CharField(required=True, allow_blank=False, style={'input_type': 'password'}, help_text='密码',
                                     label='密码', write_only=True)
    email_or_mobile = serializers.CharField(allow_blank=False, write_only=True)

    def validate_code(self, code):
        # 验证码在数据库中是否存在，用户从前端post过来的值都会放入initial_data里面，排序(最新一条)。
        type = (self.initial_data['email_or_mobile'])
        verify_records = None
        if type == 'mobile':
            verify_records = VerifyCode.objects.filter(mobile=self.initial_data["user_phone"]).order_by("-add_time")

        elif type == 'email':
            verify_records = VerifyCode.objects.filter(mobile=self.initial_data["user_phone"]).order_by("-add_time")

        if verify_records:
            # 获取到最新一条
            last_record = verify_records[0]

            # 有效期为五分钟。
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码不存在")

    def validate(self, attrs):
        # attrs["mobile"] = attrs["username"]
        # del attrs["code"]
        # return attrs
        '''
        不加字段名的验证器作用于所有字段之上，可以做一些全局的处理
        :param attrs: attrs是字段 validate之后返回的总的dict
        :return:
        '''
        if attrs['email_or_mobile'] == 'mobile':
            attrs['username'] = attrs['user_phone']
        elif attrs['email_or_mobile'] == 'email':
            attrs['username'] = attrs['user_phone']
            attrs['email'] = attrs['user_phone']
            attrs['user_phone'] = None
        del attrs['code']
        del attrs['email_or_mobile']
        '''
        这里注意一定要删除，否则下面错误：提示数据库中没有该字段
        Got AttributeError when attempting to get a value for field `code` on serializer `UserRegSerializer`.
        The serializer field might be named incorrectly and not match any attribute or key on the `UserProfile` instance.
        Original exception text was: 'UserProfile' object has no attribute 'code'.
        '''
        return attrs

    def create(self, validated_data):
        '''
        不适用signals实现，因为在update时也会调用signals，会出现bug
        :param validated_data:
        :return:
        '''
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("user_phone","code", "password", "email_or_mobile", "username", "email", )  # DRF web表单显示字段


class UserUpdateSerializer(serializers.ModelSerializer):
    '''
    注册完后完善信息
    '''

    class Meta:
        model = User
        fields = ("username", "user_gender", "user_school", "user_major", "user_phone", "user_number","user_image","user_url")  # DRF web表单显示字段

class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情序列化
    '''

    class Meta:
        model = User
        fields = (
            'id','username', 'user_phone', 'user_gender', 'user_number', 'email', 'user_school', 'user_major', 'user_url',
            'user_image', 'last_login','user_registertime')


class SmsSerializer(serializers.Serializer):
    '''
    验证某些字段
    '''
    mobile = serializers.CharField(max_length=11, label='手机号', help_text='请输入手机号')

    def validate_mobile(self, phone):
        """
        验证手机号码(函数名称必须为validate_ + 字段名)
        """
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, phone):
            raise serializers.ValidationError("手机号码非法")

        # 手机是否注册
        if User.objects.filter(user_phone=phone).exists():
            raise serializers.ValidationError("手机号已经被注册")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=phone).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return phone


class EmailSerializer(serializers.Serializer):
    '''
    对邮箱格式等进行验证
    '''
    mobile = serializers.CharField(max_length=25, label='邮箱', help_text='请输入邮箱')

    def validate_mobile(self, email):

        if not re.match(REGEX_EMAIL, email):
            raise serializers.ValidationError("邮箱格式非法")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("该邮箱已经被注册")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=email).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return email


class LogSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    user_login_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    user_login_ip = serializers.CharField(read_only=True)
    user_login_agent = serializers.CharField(read_only=True)
    user_login_os = serializers.CharField(read_only=True)


    class Meta:
        model = UserLoginLog
        fields = '__all__'
