#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : urls.py
Description      : 
Time             : 2023/08/27 19:09:48
Author           : AllenLuo
Version          : 1.0
'''


from django.urls import path
from chatgpt_image.views import Image

urlpatterns = [
    path("send", Image.as_view({"post": "create"})),
]
