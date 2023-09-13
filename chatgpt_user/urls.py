#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : urls.py
Description      : 
Time             : 2023/08/05 22:17:00
Author           : AllenLuo
Version          : 1.0
'''

from django.urls import path
from chatgpt_user.views import RegisterModelViewSet, verifyEmailCodeViewSet, CaptchaView, LoginViewSet, UserInfoViewSet
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/email", RegisterModelViewSet.as_view({"post": "create"})),
    path("get_pic_code", CaptchaView.as_view()),
    path("verify_email_code", verifyEmailCodeViewSet.as_view({"get": "list"})),
    path("login/email", LoginViewSet.as_view({"post": "create"})),
    path("info", UserInfoViewSet.as_view({"get": "list"})),
    # path('token', ObtainTokenPairViewSet.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("login", LoginViewSet.as_view({"post": "create"}))

]
