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

class LimitedAccessPermission(BasePermission):
    def has_permission(self, request, view):
        # 检查用户是否为VIP且是否在有效期内
        if request.user.VIP_TYPE == 1 and request.user.vip_expire_at > datetime.now():
            logger.info(f"{request.user.username}-未过期的VIP用户,允许访问")
            return True
        else:
            # 非vip用户或已过期用户只允许每天调用5次
            logger.info(f"{request.user.username}-普通用户用户,有限的允许访问")
            res = FrontUserBase.objects.filter(id=request.user.id).first()
            if res.call_count < 5:
                logger.info(res.call_count)
                res.call_count+=1
                res.save()
                return True

        return False


