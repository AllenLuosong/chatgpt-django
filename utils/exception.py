#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : exception.py
Description      : 
Time             : 2023/09/02 22:00:29
Author           : AllenLuo
Version          : 1.0
'''

from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotAuthenticated
from utils.json_response import ErrorResponse

def Custom_exception_handler(ex, context):
  """自定义异常处理
  """
  msg = ''
  code = 400

  if isinstance(ex, AuthenticationFailed):
      code = 401
      msg = '不正确的登录授权,请重新登录'

  elif isinstance(ex, NotAuthenticated):
      code = 401
      msg = '登录凭证不正确,请重新登录'

  elif isinstance(ex, PermissionDenied):
      code = 403
      msg = '今日访问次数已达到最大,请联系管理员'

  elif isinstance(ex, BaseException):
      msg = str(ex)

  return ErrorResponse(msg=msg, code=code)

