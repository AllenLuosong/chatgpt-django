#!usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
Filename         : views.py
Description      : 
Time             : 2023/08/13 14:34:06
Author           : AllenLuo
Version          : 1.0
'''


from chatgpt_user.serializers import LoginSerializer, RegisterDetailSerializer, UserInfoSerializer, CustomerTokenObtainPairSerializer
from utils.viewset import CustomModelViewSet
from utils.json_response import DetailResponse, ErrorResponse
from .models import FrontUserExtraEmail, CustomerCaptchaStore, EmailVerifyCode, FrontUserBase
from loguru import logger
from django.utils import timezone
import base64
from rest_framework.decorators import action
from captcha.views import captcha_image
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import string
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from faker import Faker
import jwt
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from rest_framework.response import Response

#开启定时工作
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 另一种方式为每天固定时间执行任务，对应代码为：
    @register_job(scheduler, 'cron', hour='1', minute='17', second='01',id='task', replace_existing=True )
    def my_job():
        # 更新所有用户的调用次数为0
        FrontUserBase.objects.all().update(call_count=0, update_datetime=datetime.datetime.now())
        logger.info("已重置所有用户的调用次数")
    scheduler.start()
except Exception as e:
    logger.error(f"定时任务异常-{e}")

def send_verification_email(request, to_email, verify_code,verify_ip, expire_at, verificationUrl):
    """ 邮件发送方法 
    """
    subject = settings.EMAIL_SUBJECT
    # 使用render_to_string函数将register_verify_email.html渲染为HTML内容
    html_content = render_to_string('register_verify_email.html', {'verificationUrl': verificationUrl})
    # 创建EmailMessage对象，并设置相关属性
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    # 设置邮件内容类型为html
    email.content_subtype = 'html'
    # 发送邮件
    email.send()
    EmailVerifyCode.objects.create(to_email_address=to_email, verify_code=verify_code, verify_ip=verify_ip, expire_at=expire_at).save()
    logger.info(f"邮件发送成功,接收人:{to_email}, 请求人IP:{verify_ip}")


class CaptchaView(APIView):
    @swagger_auto_schema(
        responses={"200": openapi.Response('获取成功')},
        security=[],
        operation_id="captcha-get",
        operation_description="图形验证码获取",
    )
    def get(self, request):
        data = {}
        hashkey = CustomerCaptchaStore.generate_key()
        picCodeSessionId = CustomerCaptchaStore.objects.filter(hashkey=hashkey).first().pic_code_seesion_id
        imgage = captcha_image(request, hashkey)
        # 将图片转换为base64
        image_base = base64.b64encode(imgage.content)
        data = {
            "picCodeSessionId": picCodeSessionId,
            "picCodeBase64": image_base.decode("utf-8"),
        }
        return DetailResponse(data=data, msg='OK')


class RegisterModelViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    serializer_class = RegisterDetailSerializer

    @swagger_auto_schema(method='post', 
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
          'identity': openapi.Schema(type=openapi.TYPE_STRING, description='用户ID，可以为邮箱，可以为手机号'),
          'password': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
          'picCodeSessionId': openapi.Schema(type=openapi.TYPE_STRING, description='图形验证码会话 ID'),
          'picVerificationCode': openapi.Schema(type=openapi.TYPE_STRING, description='图片验证码'),
          'registerType': openapi.Schema(type=openapi.TYPE_STRING, enum=['email', 'phone'], description='注册类型: email, phone'),
        },
        required=['custom_field'],
        responses={"200": openapi.Response("注册成功")},
    ))
    @action(methods=['POST'],detail=False)
    def create(self, request):
        """ 注册方法
        """
        username = request.data.get('identity',None)
        if not username:
            return ErrorResponse(msg="账号不能为空")
        password = request.data.get('password',None)
        if not password:
            return ErrorResponse(msg="密码不能为空")
        picVerificationCode = request.data.get('picVerificationCode',None)
        if not picVerificationCode:
            return ErrorResponse(msg="验证码不能为空")

        picCodeSessionId = request.data.get('picCodeSessionId',None)
        try:
          self.image_code = CustomerCaptchaStore.objects.filter(pic_code_seesion_id=picCodeSessionId).first()
          self._expiration = CustomerCaptchaStore.objects.get(pic_code_seesion_id=picCodeSessionId).expiration
          if  timezone.now()  > self._expiration:  # 先判断是否过期
            return ErrorResponse(msg="验证码过期,请刷新重试") 
          elif  self.image_code and (self.image_code.response == picVerificationCode or self.image_code.challenge == picVerificationCode):
              self.image_code.delete() # 验证通过将数据库存储的验证码删除
          else:
              return ErrorResponse(msg="验证码错误,请输入正确的验证码")
        except:
              return ErrorResponse(msg="验证码错误,请刷新重试")


        salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        record, b = FrontUserExtraEmail.objects.get_or_create(username=username, verified=1, 
            defaults={            
            'password':self.set_password(password,salt),
            'salt': salt,
             'verified': 0
            })
        if not b:
            msg = "该账号已注册,请登录"
            logger.warning(f"{username}-该账号已注册,请登录")
            return ErrorResponse(msg=msg)
        # FrontUserExtraEmail.objects.create(username=username, password=self.set_password(password,salt), salt=salt).save()
        verify_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        verificationUrl = settings.VERIFICATION_REDIRECT_URL + verify_code
        expire_at = timezone.now() + datetime.timedelta(minutes=int(settings.EMAIL_TIMEOUT))
        verify_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        send_verification_email(request, username, verify_code, verify_ip, expire_at, verificationUrl)
        return DetailResponse(data={})


    def set_password(self, raw_password, salt):
        """
        Description: 密码加密方法
        ---------
        Arguments: raw_password： 原始密码
                   salt： 加密盐
        ---------
        Returns:   使用加密盐加密之后的密码
        -------
        """
        salted_password = make_password(raw_password, salt)
        return salted_password


    def check_password(self, password, salted_password) -> bool:
        """ 密码解密方法
        """
        is_valid = check_password(password, salted_password)
        return is_valid

class verifyEmailCodeViewSet(CustomModelViewSet):
    """ 校验邮件验证码方法
    """
    serializer_class = UserInfoSerializer

    def list(self, request):
      verifyCode = request.GET.get('code')
      verifyCode_value = EmailVerifyCode.objects.filter(verify_code=verifyCode, expire_at__gt=timezone.now()).first()
      if verifyCode_value:
          username = EmailVerifyCode.objects.filter(verify_code=verifyCode_value.verify_code).first().to_email_address
          # 核销认证通过
          res = FrontUserExtraEmail.objects.filter(username=username).first()
          res.verified = 1 # 先更新认证状态
          res.update_datetime = timezone.now()
          res.save()   

          # 获取最新一次注册时使用的密码及加密盐
          password = res.password
          salt = res.salt

          faker = Faker()
          faker.word()
          nikename = "ChatAI_" + faker.word()
          ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
          # 邮箱验证通过写入用户基础信息表
          FrontUserBase.objects.create(username=username, nickname=nikename, password=password, salt=salt, last_login_ip=ip)
          msg = f"{username}注册邮件核销成功"
          logger.info(msg)
          return DetailResponse(msg)
      else:
          return ErrorResponse(msg='验证码过期或不存在,请重新注册')


class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # 使用自定义用户信息生成Token的逻辑
        # 返回一个唯一标识用户的字符串
        return f"{user.id}{timestamp}"
    


class LoginViewSet(CustomModelViewSet):
    """
    登录接口
    """
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        username = request.data.get('username',None)
        if username is None:
            return ErrorResponse(msg="账号不能为空")
        password = request.data.get('password',None)
        if password is None:
            return ErrorResponse(msg="密码不能为空")
        user = FrontUserExtraEmail.objects.filter(username=username).first()
        res = FrontUserBase.objects.filter(username=username).first()

        if not res:  # 检查账号是否存在及是否验证完成
            logger.warning(f"{username}未注册")
            return ErrorResponse(msg='账号未注册')
        if user.verified != 1:
            logger.warning(f"{username}注册流程未完成")
            return ErrorResponse(msg='注册流程未完成,请完成注册或重新注册')
        
        salted_password = res.password
        if not check_password(password, salted_password):    # 检查密码是否正确
            logger.warning(f"{user}账号/密码不匹配")
            return ErrorResponse(msg='账号/密码不匹配')
        token = LoginSerializer.get_token(res).access_token  # 生成access_token
        baseUserId = res.id
        result = {
            "token": str(token),
            "baseUserId": baseUserId,
        }
        logger.success(f"{username}登录成功")
        return DetailResponse(data=result)


class UserInfoViewSet(CustomModelViewSet):
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        customer_id=decoded_token["id"]
        res = FrontUserBase.objects.filter(id=customer_id).first()
        result = {
                "baseUserId": customer_id,
                "nickname": res.nickname,
                "email": res.username,
                "description": res.description,
                "avatarUrl": res.avatar_version
        }
        return DetailResponse(data=result)


