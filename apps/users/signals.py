#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/21 上午 10:21

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:  #如果是新建
        password = instance.password
        instance.set_password(password)
        instance.save()
