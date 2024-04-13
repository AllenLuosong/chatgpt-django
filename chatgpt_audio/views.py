#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : views.py
Description      : 
Time             : 2024/04/09 21:37:38
Author           : AllenLuo
Version          : 1.0
'''


from django.shortcuts import render
from rest_framework import permissions
from utils.json_response import ErrorResponse, DetailResponse
from utils.permisson import LimitedAccessPermission
from rest_framework.viewsets import ModelViewSet
from django_restql.mixins import QueryArgumentsMixin
from openai import OpenAI
from loguru import logger
from chatgpt_config.models import Config

class Audio(ModelViewSet,QueryArgumentsMixin):
  permission_classes = [permissions.IsAuthenticated, LimitedAccessPermission] # 登录授权才可以访问接口

  def create(self, request):
    openai_chat_api_3_5_config = Config.objects.filter(config_Code='openai_chat_api_3_5')
    openai_chat_api_3_5_config_dict = {}
    for i in openai_chat_api_3_5_config:
      openai_chat_api_3_5_config_dict.update({i.key: i.value})
    client = OpenAI(
      api_key = openai_chat_api_3_5_config_dict.get("OPENAI_API_KEY", 'None'),
      base_url = openai_chat_api_3_5_config_dict.get("OPENAI_API_BASE_URL", 'None')
    )

    logger.info(request.FILES['file'])
    # fileBuffer
    audio_file = open(request.FILES['file'].read(), "rb")
    transcript = client.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file
    )
    logger.info(transcript)
    return DetailResponse(data=transcript, msg="Success")
