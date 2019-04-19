#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/15 下午 02:07

import uuid
for i in range(10):
    a = uuid.uuid1()
    print(a)
    print(len(str(a)))