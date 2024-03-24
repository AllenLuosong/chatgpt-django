#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : permisson.py
Description      : 自定义权限
Time             : 2023/09/01 22:14:14
Author           : AllenLuo
Version          : 1.0
'''

from datetime import datetime
from rest_framework.permissions import BasePermission
from loguru import logger
from chatgpt_user.models import UserBenefits
from chatgpt_config.models import Config

class LimitedAccessPermission(BasePermission):
    def has_permission(self, request, view):
        # 检查用户是否为VIP
        if request.user.VIP_TYPE == 1:
            return True
        else:
            res = UserBenefits.objects.filter(baseUserId=request.user.id).first()
            if res.left_tokens <= 0 or res.left_dalle <= 0: # 非vip用户允许的额度
                logger.info(f"用户{request.user.username}剩余使用次数不足: left_tokens-{res.left_tokens}, left_dalle-{res.left_dalle}")
                return False

        return True


