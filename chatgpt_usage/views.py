from django.shortcuts import render
from utils.viewset import CustomModelViewSet
from rest_framework import permissions
from chatgpt_config.models import UserConfig
from chatgpt_chat.models import ChatMessage
from utils.json_response import DetailResponse, ErrorResponse
import requests
from loguru import logger
import json
from django.utils import timezone
from django.db.models import Sum
from chatgpt_usage.throttles import *

# Create your views here.
"""
curl --location --request GET ' https://api.openai-proxy.org/dashboard/billing/credit_grants' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer sk-xxxx'
"""

class Usage(CustomModelViewSet):
  permission_classes = [permissions.IsAuthenticated]
  throttle_classes = [UsageAnonRateThrottle, UsageUserRateThrottle]

  def list(self, request):
    baseUserId = request.user.id
    user_config = UserConfig.objects.filter(baseUserId=baseUserId).first()
    if user_config.secretKey:
      secretKey = user_config.secretKey
      headers = {
                "Authorization": f"Bearer {secretKey}",
                 "Content-Type": "application/json"
                 }
      url = user_config.proxyAdress.rsplit('/',1)[0] + '/dashboard/billing/credit_grants'
      response = requests.request('GET', url=url, headers=headers)
      return DetailResponse(data=response.json())
    
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


