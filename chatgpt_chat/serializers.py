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


class ChatMessageSend(CustomModelSerializer):
    """
    序列化器
    """
    code = serializers.CharField()
    message = serializers.CharField()

    class Meta:
        model = ChatMessage
        fields = "__all__"