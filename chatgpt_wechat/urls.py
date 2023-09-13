#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : urls.py
Description      : 
Time             : 2023/09/08 15:05:49
Author           : AllenLuo
Version          : 1.0
'''


from django.urls import path
from chatgpt_wechat.views import Wechat
urlpatterns = [
    path("", Wechat.as_view({"get": "get"})),
]

