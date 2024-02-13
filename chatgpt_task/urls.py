#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : urls.py
Description      : 
Time             : 2024/02/13 16:01:30
Author           : AllenLuo
Version          : 1.0
'''


from django.urls import path
from chatgpt_task.views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
]

