#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : urls.py
Description      : 
Time             : 2023/08/05 22:17:00
Author           : AllenLuo
Version          : 1.0
'''

from django.urls import path
from chatgpt_chat.views import Chat

urlpatterns = [
    path("send", Chat.as_view({"post": "creat"})),
]
