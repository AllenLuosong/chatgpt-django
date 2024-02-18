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
from chatgpt_user.models import FrontUserBase
from chatgpt_config.models import Config

class LimitedAccessPermission(BasePermission):
    def has_permission(self, request, view):
        # 检查用户是否为VIP且是否在有效期内
        if request.user.VIP_TYPE == 1 and request.user.vip_expire_at > datetime.now():
            logger.info(f"{request.user.username}-未过期VIP用户,允许访问")
            return True
        else:
            res = FrontUserBase.objects.filter(id=request.user.id).first()
            PermissionDeniedNum = Config.objects.filter(key="PermissionDeniedNum").first()
            if res.call_count < int(PermissionDeniedNum.value): # 非vip用户或已过期用户只允许每天调用次数
                res.call_count+=1
                logger.info(f"{request.user.username}-普通用户,有限的访问,当前访问次数-{res.call_count}")
                res.save()
                return True

        return False


