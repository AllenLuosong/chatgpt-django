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
from chatgpt_image.models import ImageMessage, FileList
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


class FileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        # 获取本地保存路径
        return str(instance.url)

    class Meta:
        model = FileList
        fields = "__all__"

    def create(self, validated_data):
        validated_data['name'] = str(self.initial_data.get('file'))
        validated_data['url'] = self.initial_data.get('file')
        return super().create(validated_data)