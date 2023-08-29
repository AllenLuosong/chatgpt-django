#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : views.py
Description      : 
Time             : 2023/08/28 09:40:20
Author           : AllenLuo
Version          : 1.0
'''


import openai  # OpenAI Python library to make API calls
from utils.viewset import CustomModelViewSet
from chatgpt_image.serializers import ImageMessageSend
from django.conf import settings
from loguru import logger
import openai
from rest_framework import permissions
from utils.json_response import DetailResponse, ErrorResponse
from django.utils.translation import gettext_lazy as _

class Image(CustomModelViewSet):
    serializer_class = ImageMessageSend
    permission_classes = (permissions.IsAuthenticated,)
    openai.api_key = settings.OPENAI_API_KEY
    openai.api_base = settings.OPENAI_API_BASE_URL
    openai_model = settings.MODEL

    def create(self, request):
        prompt = request.data["prompt"]
        n = request.data["n"]
        size = request.data["size"]
        logger.info(f"prompt-{prompt}")
        try:
            generation_response = openai.Image.create(
                prompt=prompt,
                n=n,
                size=size,
                request_timeout = 30
            )
            logger.info(generation_response)
            return DetailResponse(data=generation_response)
        except BaseException as e:
            msg="请求失败,请稍后再试"
            logger.error(f'{msg}-后台返回-{e}')
            return ErrorResponse(code=500, data={}, msg=msg)