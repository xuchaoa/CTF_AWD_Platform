#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 19-5-18 下午2:24
# @Author  : Archerx
# @Site    : https://blog.ixuchao.cn
# @File    : celery_test.py
# @Software: PyCharm


from celery_tasks.SendCode import tasks as SendCode


if __name__ == '__main__':
    SendCode.SendMail.delay('112566',['755563428@qq.com'])

    print('main over')
