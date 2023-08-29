#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : serializers.py
Description      : 
Time             : 2023/08/28 09:23:53
Author           : AllenLuo
Version          : 1.0
'''


from utils.serializers import CustomModelSerializer
from rest_framework import serializers
from chatgpt_image.models import ImageMessage
from django.utils.translation import gettext_lazy as _


class ImageMessageSend(CustomModelSerializer):
    """
    序列化器
    """
    n = serializers.IntegerField(default=1)
    size = serializers.CharField(default="512x512")
    prompt = serializers.CharField(default="A cyberpunk monkey hacker dreaming of a beautiful bunch of bananas, digital art")


    class Meta:
        model = ImageMessage
        fields = ("size", "n", "prompt",)