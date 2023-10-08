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
from chatgpt_image.serializers import ImageMessageSend, FileSerializer
from django.conf import settings
from loguru import logger
import openai
from rest_framework import permissions
from utils.json_response import DetailResponse, ErrorResponse
from django.utils.translation import gettext_lazy as _
from utils.permisson import LimitedAccessPermission
from chatgpt_image.models import FileList, ImageMessage
import os
from chatgpt_bootstrap.settings import BASE_DIR
import uuid
import datetime
from chatgpt_image.tasks import put_openai_image_to_superbed


class Image(CustomModelViewSet):
    serializer_class = ImageMessageSend
    permission_classes = [permissions.IsAuthenticated, LimitedAccessPermission]
    openai.api_key = settings.OPENAI_API_KEY
    openai.api_base = settings.OPENAI_API_BASE_URL
    superbed_token = settings.SUPERBED_TOKEN


    def generate_uuid(self, request):
        """ 返回一个用于创建图片的uuid
        """
        serializer = ImageMessageSend(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uuid_str = str(uuid.uuid4()).replace("-", "")
            req_data = serializer.validated_data
            serializer.save(number=req_data['number'], size=req_data['size'],
                            prompt=req_data['prompt'], username=request.user.username, uuid=uuid_str)
            result = {
                "uuid": uuid_str
            }
            return DetailResponse(data=result)

    def image_detail(self, request, uuid):
        """ 获取图片url
        """
        imagemessage = ImageMessage.objects.filter(uuid=uuid).first()
        serializer = ImageMessageSend(imagemessage)
        logger.debug(serializer.data)
        generation_response = openai.Image.create(
            prompt=serializer.data['prompt'],
            n=serializer.data['number'],
            size=serializer.data['size']
          )

        logger.info(generation_response)
        url_list = [url["url"] for url in  generation_response["data"] ]
        put_openai_image_to_superbed.delay(uuid, url_list)

        dt_object = datetime.datetime.fromtimestamp(
            generation_response['created'])
        createTime = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        result = {
            "createTime": createTime,
            "imageUrlList": generation_response['data'],
            "uuid": f"{uuid}"
        }
        return DetailResponse(data=result)

    def images_list(self, request):
        imagemessage = ImageMessage.objects.filter(username=request.user.username)[:10]
        logger.debug(imagemessage)
        serializer = ImageMessageSend(imagemessage)
        return DetailResponse(serializer.data)

    def edit(self, request):
        """修图
        """
        n = request.data["number"]
        size = request.data["size"]
        prompt = request.data["prompt"]
        originalImage_path = os.path.join(
            BASE_DIR, request.data["originalImage"])
        maskImage_path = os.path.join(BASE_DIR, request.data["maskImage"])
        logger.debug(originalImage_path)
        logger.debug(maskImage_path)
        try:
            image_response = openai.Image.create_edit(
                image=open(originalImage_path, "rb"),
                mask=open(maskImage_path, "rb"),
                prompt=prompt,
                n=n,
                size=size
            )
            logger.debug(image_response)
            return DetailResponse(data=image_response)
        except BaseException as e:
            msg = "请求失败,请稍后再试"
            logger.error(f'{msg}-后台返回-{e}')
            return ErrorResponse(code=500, data={}, msg=msg)

    def variation(self, request):
        """以图生图
        """
        n = request.data["number"]
        size = request.data["size"]
        originalImage_path = os.path.join(
            BASE_DIR, request.data["originalImage"])
        try:
            logger.debug(originalImage_path)
            image_response = openai.Image.create_variation(
                image=open(originalImage_path, "rb"),
                n=n,
                size=size
            )
            logger.debug(image_response)
            return DetailResponse(data=image_response)
        except BaseException as e:
            msg = "请求失败,请稍后再试"
            logger.error(f'{msg}-后台返回-{e}')
            return ErrorResponse(code=500, data={}, msg=msg)


class FileViewSet(CustomModelViewSet):
    """
    文件管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = FileList.objects.all()
    serializer_class = FileSerializer
    filter_fields = ['name', ]
    permission_classes = []
