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
from chatgpt_image.views import Image, FileViewSet
from rest_framework import routers
from utils.router_url import StandardRouter

system_url = StandardRouter()
system_url.register(r'upload', FileViewSet)

urlpatterns = [
    path("generation", Image.as_view({"post": "create"})),
    path("edit", Image.as_view({"post": "edit"})),
    path("variation", Image.as_view({"post": "variation"})),

] + system_url.urls
