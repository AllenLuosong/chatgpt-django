#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : serializers.py
Description      : 
Time             : 2023/08/14 16:49:52
Author           : AllenLuo
Version          : 1.0
'''

from utils.serializers import CustomModelSerializer
from rest_framework import serializers
from chatgpt_chat.models import ChatMessage


class ChatMessageSerializers(serializers.ModelSerializer):
    """
    序列化器
    """
    baseUserId = serializers.IntegerField(required=False)
    prompt = serializers.CharField()
    completion = serializers.CharField(allow_blank=True, required=False)
    prompt_tokens = serializers.IntegerField(required=False)
    total_tokens = serializers.IntegerField(required=False)
    completion_tokens = serializers.IntegerField(required=False)
    chat_model = serializers.CharField(allow_blank=True, required=False)
    
    class Meta:
        model = ChatMessage
        fields = "__all__"