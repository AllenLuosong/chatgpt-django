from django.shortcuts import render
from utils.viewset import CustomModelViewSet
from rest_framework import permissions
from chatgpt_config.models import UserConfig
from chatgpt_chat.models import ChatMessage
from utils.json_response import DetailResponse, ErrorResponse
import requests
from loguru import logger
from django.utils import timezone
from django.db.models import Sum
from chatgpt_usage.throttles import *
from chatgpt_image.models import ImageMessage
# Create your views here.

class Usage(CustomModelViewSet):
  permission_classes = [permissions.IsAuthenticated]
  # throttle_classes = [UsageAnonRateThrottle, UsageUserRateThrottle]

  def list(self, request):
    baseUserId = request.user.id
    user_config = UserConfig.objects.filter(baseUserId=baseUserId).first()
    current_year = timezone.now().year
    current_month = timezone.now().month
    # 今日请求图片
    today_user_image_usage = ImageMessage.objects.filter(baseUserId=baseUserId, create_datetime__day=timezone.now().day).aggregate(nums=Sum('number'))
    # 当月请求数
    mothly_user_image_usage = ImageMessage.objects.filter(baseUserId=baseUserId, create_datetime__year=current_year, create_datetime__month=current_month).aggregate(nums=Sum('number'))
    # 今日消耗tokens
    today_user_usage = ChatMessage.objects.filter(baseUserId=baseUserId, created=timezone.now().date()).aggregate(nums=Sum('total_tokens'))
    # 当月消耗tokens
    mothly_user_usage = ChatMessage.objects.filter(baseUserId=baseUserId, created__year=current_year, created__month=current_month).aggregate(nums=Sum('total_tokens'))
    data = {
            "today_user_usage": today_user_usage.get('nums', '0'), 
            "mothly_user_usage": mothly_user_usage.get('nums', '0'),
            "today_user_image_usage": today_user_image_usage.get('nums', '0'),
            "mothly_user_image_usage": mothly_user_image_usage.get('nums', '0')
            }
    if user_config.secretKey:
      secretKey = user_config.secretKey
      headers = {
                "Authorization": f"Bearer {secretKey}",
                 "Content-Type": "application/json"
                 }
      url = user_config.proxyAdress.rsplit('/',1)[0] + '/dashboard/billing/credit_grants'
      response = requests.request('GET', url=url, headers=headers)
      data.update(response.json())
      return DetailResponse(data=data)
    else:
      return DetailResponse(data=data)


  def userUsage(self, request):
    baseUserId = request.user.id
    current_year = timezone.now().year
    current_month = timezone.now().month
    today_user_usage = ChatMessage.objects.filter(baseUserId=baseUserId, created=timezone.now().date()).aggregate(nums=Sum('total_tokens'))
    mothly_user_usage = ChatMessage.objects.filter(baseUserId=baseUserId, created__year=current_year, created__month=current_month).aggregate(nums=Sum('total_tokens'))
    logger.info(today_user_usage['nums'])
    logger.info(mothly_user_usage['nums'])
    data = {"today_user_usage": today_user_usage, "mothly_user_usage": mothly_user_usage}
    return DetailResponse(data=data)
