#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-13 上午10:31
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : CustomBackend.py
# @Software: PyCharm



from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()  # 获取setting.py中AUTH_USER_MODEL指定的User model

class UserCustomBackend(ModelBackend):
    '''
    自定义用户验证(全局配置就行)
    我们可以使用符号&或者|将多个Q()对象组合起来传递给filter()，exclude()，get()等函数。当多个Q()对象组合起来时，Django会自动生成一个新的Q()
    tips: 测试完成
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(user_phone=username) | Q(email=username))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None
