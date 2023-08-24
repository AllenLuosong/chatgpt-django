#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : views.py
Description      : 
Time             : 2023/08/15 22:15:23
Author           : AllenLuo
Version          : 1.0
'''

from django.http import StreamingHttpResponse
from utils.viewset import CustomModelViewSet
from chatgpt_chat.serializers import ChatMessageSend
import uuid
import json
import time
from django.conf import settings
from loguru import logger
import openai
from rest_framework import permissions
from django.http import HttpResponse

class Chat(CustomModelViewSet):
    serializer_class = ChatMessageSend
    permission_classes = (permissions.IsAuthenticated,)

    def creat(self, request):
        prompt = request.data.get("prompt")
        logger.info(f"prompt-{prompt}")
        # openai.api_key = settings.OPENAI_API_KEY
        # completion = openai.ChatCompletion.create(
        #   api_base = settings.OPENAI_API_BASE_URL,
        #   model="gpt-3.5-turbo",
        #   messages=[
        #     {"role": "system", "content": "You are a helpful assistant."},
        #     {"role": "user", "content": prompt }
        #   ],
        #   request_timeout = 30,
        #   # stream=True
        # )
        # for chunk in completion:
        #   logger.info(chunk.choices[0].delta)
        # text = completion.choices[0].message.content
        # logger.info(f"completion-{completion}")
        text = "我是一个AI助手，可以帮助您回答问题和提供信息。有什么我可以帮助您的吗我是一个AI助手，可以帮助您回答问题和提供信息。有什么我可以帮助您的吗我是一个AI助手，可以帮助您回答问题和提供信息。有什么我可以帮助您的吗我是一个AI助手，可以帮助您回答问题和提供信息。有什么我可以帮助您的吗我是一个AI助手，可以帮助您回答问题和提供信息。有什么我可以帮助您的吗"
        def generate_text(text=text):
            # 流媒体文本处理方法
            id = str(uuid.uuid4()),
            parentMessageId = str(uuid.uuid4()),
            conversationId = str(uuid.uuid4()),
            for i in range(len(text)):
                data = {
                    "role": "null",
                    "id": id[0],
                    "parentMessageId": parentMessageId[0],
                    "conversationId": conversationId[0],
                    "text": text[:i+1],
                }
                yield str(json.dumps(data, ensure_ascii=False)) + '\n'
                time.sleep(0.05)
        response = StreamingHttpResponse(streaming_content=generate_text(), content_type='application/octet-stream')
        return response
