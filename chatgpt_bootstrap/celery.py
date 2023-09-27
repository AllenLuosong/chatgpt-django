#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : celery.py
Description      : 
Time             : 2023/09/21 19:35:17
Author           : AllenLuo
Version          : 1.0
'''


import os
from celery import Celery

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatgpt_bootstrap.settings')

# 实例化
app = Celery('chatgpt_bootstrap')

# namespace='CELERY'作用是允许你在Django配置文件中对Celery进行配置
# 但所有Celery配置项必须以CELERY开头，防止冲突
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从Django的已注册app中发现任务
app.autodiscover_tasks()
