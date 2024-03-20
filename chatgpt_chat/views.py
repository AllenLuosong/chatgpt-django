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
from chatgpt_chat.serializers import ChatMessageSerializers
from chatgpt_config.serializers import UserConfigserializer
import uuid
import json
import time
from django.conf import settings
from loguru import logger
import openai
from rest_framework import permissions
from utils.json_response import ErrorResponse
from utils.permisson import LimitedAccessPermission
from chatgpt_config.models import Config, UserConfig
import json
from chatgpt_user.models import UserBenefits, FrontUserBase
from anthropic import Anthropic

class Chat(CustomModelViewSet):
    serializer_class = ChatMessageSerializers
    permission_classes = [permissions.IsAuthenticated, LimitedAccessPermission] # 登录授权才可以访问接口


    def create(self, request):
        baseUserId = request.user.id
        user_config = UserConfig.objects.filter(baseUserId=baseUserId)
        res = FrontUserBase.objects.filter(id=baseUserId).first()
        serializer = UserConfigserializer(user_config.first())
        openai_chat_api_3_5_config = Config.objects.filter(config_Code='openai_chat_api_3_5')
        openai_chat_api_3_5_config_dict = {}
        for i in openai_chat_api_3_5_config:
          openai_chat_api_3_5_config_dict.update({i.key: i.value})
        logger.info(serializer.data)
        prompt = request.data["prompt"]
        if serializer.data['chatModel'].startswith('gpt'):
          # chatgpt 处理逻辑
          if serializer.data.get('secretKey', 'None'):
            # 自定义代理处理逻辑
            openai.api_key = serializer.data.get('secretKey', 'None')
            openai.api_base = serializer.data.get('proxyAdress', 'None')
            openai_model = serializer.data.get('chatModel', 'None')

          elif res.VIP_TYPE == 1:
            # 会员处理逻辑
            openai.api_key = openai_chat_api_3_5_config_dict.get("OPENAI_API_KEY", 'None')
            openai.api_base = openai_chat_api_3_5_config_dict.get("OPENAI_API_BASE_URL", 'None')
            openai_model = serializer.data.get('chatModel', 'None')
          
          else:
            openai.api_key = openai_chat_api_3_5_config_dict.get("OPENAI_API_KEY", 'None')
            openai.api_base = openai_chat_api_3_5_config_dict.get("OPENAI_API_BASE_URL", 'None')
            openai_model = openai_chat_api_3_5_config_dict.get("model", 'None')

          serializer = ChatMessageSerializers(data=request.data)

          if serializer.is_valid(raise_exception=True):
            logger.info(serializer.validated_data)
          try:
              completion = openai.ChatCompletion.create(
                  model= openai_model,
                  messages=[
                      {"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}
                  ],
                  request_timeout = 45,
              )
              logger.info(f"completion-{completion}")
              chat_text = completion.choices[0].message.content
              prompt_tokens = completion.usage.prompt_tokens
              completion_tokens = completion.usage.completion_tokens
              total_tokens = completion.usage.total_tokens
              serializer.save(prompt=prompt,baseUserId=request.user.id,completion=completion,chat_model=openai_model,
                  prompt_tokens=prompt_tokens,completion_tokens=completion_tokens,total_tokens=total_tokens)

              res = UserBenefits.objects.filter(baseUserId=baseUserId).first() # 更新用户福利表
              res.left_tokens -=total_tokens
              res.save()

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
                      time.sleep(0.02)
              response = StreamingHttpResponse(streaming_content=generate_streaming_text(), content_type='application/octet-stream')
              return response
          except BaseException as e:
              msg="请求失败,请稍后再试"
              logger.error(f'{msg}-后台返回-{e}')
              return ErrorResponse(code=500, data={}, msg=msg)
          
        elif serializer.data['chatModel'].startswith('claude'):                  
          # claude 处理逻辑
          client = Anthropic(
              api_key = openai_chat_api_3_5_config_dict.get("OPENAI_API_KEY", 'None'),
              base_url = 'https://api.openai-proxy.org/anthropic'
          )

          message = client.messages.create(
              max_tokens=1024,
              messages=[
                  {
                      "role": "user",
                      "content": prompt,
                  }
              ],
              model= serializer.data.get('chatModel', 'None'),
          )
          logger.info(message.content[0].text)
          def generate_streaming_text(text=message.content[0].text):
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
                      time.sleep(0.02)
          response = StreamingHttpResponse(streaming_content=generate_streaming_text(), content_type='application/octet-stream')
          return response