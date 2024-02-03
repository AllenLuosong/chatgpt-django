from django.shortcuts import render
from utils.viewset import CustomModelViewSet
from rest_framework import permissions
from chatgpt_config.serializers import Configserializer, ConfigEditserializer, UserConfigserializer
from chatgpt_config.models import UserConfig
from utils.json_response import DetailResponse, ErrorResponse
from loguru import logger

class ConfigView(CustomModelViewSet):
  serializer_class = Configserializer
  permission_classes = [permissions.IsAuthenticated]

  def list(self, request):
    baseUserId = request.user.id
    user_config = UserConfig.objects.filter(baseUserId=baseUserId).first()
    serializer = UserConfigserializer(user_config)
    return DetailResponse(data=serializer.data)
  
  def edit(self, request):
    serializer = ConfigEditserializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      user_config = UserConfig.objects.filter(baseUserId=serializer.validated_data['baseUserId']).first()
      if user_config:
        validated_data = {
                          'secretKey': serializer.validated_data['secretKey'],
                          'proxyAdress': serializer.validated_data['proxyAdress'],
                          'baseUserId': serializer.validated_data['baseUserId'],
                          'chatModel': serializer.validated_data['chatModel'], 
                          'drawvalue': serializer.validated_data['drawvalue']
                          }
        serializer.update(user_config, validated_data)
      else:
        serializer.save(secretKey=serializer.validated_data['secretKey'],
                        proxyAdress=serializer.validated_data['proxyAdress'],
                        baseUserId=serializer.validated_data['baseUserId'], 
                        chatModel=serializer.validated_data['chatModel'], 
                        drawvalue=serializer.validated_data['drawvalue'])
      return DetailResponse()

