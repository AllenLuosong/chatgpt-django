#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : views.py
Description      : 
Time             : 2023/09/08 17:37:07
Author           : AllenLuo
Version          : 1.0
'''


from django.shortcuts import render
from utils.viewset import CustomModelViewSet
from rest_framework import permissions
from loguru import logger
from utils.json_response import DetailResponse, ErrorResponse
import hashlib
from rest_framework.response import Response

# Create your views here.

class Wechat(CustomModelViewSet):
    permission_classes = [permissions.AllowAny] # 登录授权才可以访问接口
    def get(self, request, *args,):
      """  微信开发者认证功能
      """
      try:
        signature = request.query_params.get('signature',None)
        echostr = request.query_params.get('echostr',None)
        timestamp = request.query_params.get('timestamp',None)
        nonce = request.query_params.get('nonce',None)
        TOKEN = 'itchatmp'
        params = [TOKEN, nonce, timestamp]
        params.sort()
        # 按字典顺序进行排序
        params.sort()
        params_str = ' '.join(params).replace(' ', '')
        logger.info(params_str)
        sha1_key = hashlib.sha1()
        sha1_key.update(params_str.encode("utf-8"))
        logger.info(signature)
        logger.info(sha1_key.hexdigest())
        if sha1_key.hexdigest() == signature:
          # data = {"echostr": echostr}
          return Response(echostr)
          # return DetailResponse(data=data)
        else:
          return ErrorResponse(msg="错误的签名")
      except Exception as e:
        logger.error(f"出现错误,请检查-{e}")
        return ErrorResponse(msg="出现错误,请稍后再试")
