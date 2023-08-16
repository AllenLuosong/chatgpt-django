#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : serializers.py
Description      : 
Time             : 2023/08/06 20:52:03
Author           : AllenLuo
Version          : 1.0
'''


from chatgpt_user.models import FrontUserExtraEmail
from utils.serializers import CustomModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterDetailSerializer(CustomModelSerializer):
    """
    序列化器
    """
    identity = serializers.CharField()
    password = serializers.CharField()
    picCodeSessionId = serializers.CharField()
    picVerificationCode = serializers.CharField()
    registerType = serializers.CharField()

    class Meta:
        model = FrontUserExtraEmail
        fields = "__all__"


class RegisterDetailCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    identity = serializers.CharField()
    password = serializers.CharField()
    picCodeSessionId = serializers.CharField()
    picVerificationCode = serializers.CharField()
    registerType = serializers.CharField()


    class Meta:
        model = FrontUserExtraEmail
        fields = "__all__"

class LoginSerializer(TokenObtainPairSerializer):
    """
    登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """
    @classmethod
    def get_token(cls, user):
        token = super(LoginSerializer, cls).get_token(user)

        # 添加额外信息
        token['username'] = user.username
        return token
    
    class Meta:
        model = FrontUserExtraEmail
        fields = ["username", "password"]
        read_only_fields = ["id"]



class CustomerTokenObtainPairSerializer(TokenObtainPairSerializer):

    class Meta:
        model = FrontUserExtraEmail
        fields = "__all__"


class UserInfoSerializer(CustomModelSerializer):
    
    class Meta:
        model = FrontUserExtraEmail
        fields = "__all__"
