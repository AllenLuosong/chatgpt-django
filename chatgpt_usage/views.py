from django.shortcuts import render
from utils.viewset import CustomModelViewSet
from rest_framework import permissions
from chatgpt_config.models import UserConfig
from chatgpt_config.serializers import UserConfigserializer
from utils.json_response import DetailResponse, ErrorResponse
import requests
from loguru import logger
import json
# Create your views here.
"""
curl --location --request GET ' https://api.openai-proxy.org/dashboard/billing/credit_grants' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer sk-xxxx'
"""

class Usage(CustomModelViewSet):
  permission_classes = [permissions.IsAuthenticated]

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


