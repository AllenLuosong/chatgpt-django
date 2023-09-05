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
from utils.json_response import ErrorResponse
from utils.permisson import LimitedAccessPermission

class Chat(CustomModelViewSet):
    serializer_class = ChatMessageSend
    permission_classes = [permissions.IsAuthenticated, LimitedAccessPermission] # 登录授权才可以访问接口
    openai.api_key = settings.OPENAI_API_KEY
    openai.api_base = settings.OPENAI_API_BASE_URL
    openai_model = settings.MODEL

    def create(self, request):
        prompt = request.data["prompt"]
        logger.info(f"prompt-{prompt}")
        try:
            # completion = openai.ChatCompletion.create(
            #     model=self.openai_model,
            #     messages=[
            #         {"role": "system", "content": "You are a helpful assistant."},
            #         {"role": "user", "content": prompt}
            #     ],
            #     request_timeout = 30,
            # )
            # logger.info(f"completion-{completion}")

            # chat_text = completion.choices[0].message.content
            chat_text  = "你好"
            def generate_streaming_text(text=chat_text):
                # 流媒体文本处理方法
                id = str(uuid.uuid4())
                parent_message_id = str(uuid.uuid4())
                conversation_id = str(uuid.uuid4())
                for i, char in enumerate(text):
                    data = {
                        "role": "null",
                        "id": id,
                        "parentMessageId": parent_message_id,
                        "conversationId": conversation_id,
                        "text": text[:i + 1],
                    }
                    yield f"{json.dumps(data, ensure_ascii=False)}\n"
                    time.sleep(0.05)
            response = StreamingHttpResponse(streaming_content=generate_streaming_text(), content_type='application/octet-stream')
            return response
        except BaseException as e:
            msg="请求失败,请稍后再试"
            logger.error(f'{msg}-后台返回-{e}')
            return ErrorResponse(code=500, data={}, msg=msg)