#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-19 下午8:01
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : exceptions.py
# @Software: PyCharm

from rest_framework.views import exception_handler as drf_exception_handler
import logging
from rest_framework.response import Response
from rest_framework import status
#所有的数据库异常都是这两个异常的儿子或孙子,导入他俩就行
from django.db import DatabaseError
from redis.exceptions import RedisError

# 获取在配置文件中定义的logger，用来记录日志
logger = logging.getLogger('django')

def exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 别的地方抛的异常就会传给exc
    :param context: 字典形式。抛出异常的上下文(即抛出异常的出处;即抛出异常的视图)
    :return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法,把异常和异常出处交给他处理,如果是序列化器异常就直接处理,处理之后就直接返回
    response = drf_exception_handler(exc, context)
	#如果响应为空表示不是序列化器异常,补充数据库异常
    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response
