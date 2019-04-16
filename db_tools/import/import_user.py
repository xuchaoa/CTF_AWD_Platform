#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/16 上午 09:07

import sys
import os


path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,path+'../../')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CTF_AWD_Platform.settings')

import django
django.setup()

from db_tools.data.user_data import user as users
from apps.x_user.models import User_Profile
for user in users:
    user_instance = User_Profile()
    user_instance.user_name = user.get('user_name')
    user_instance.user_school = user.get('user_school')
    user_instance.save()



