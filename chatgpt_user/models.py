from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from captcha.views import CaptchaStore
from django.contrib.auth.models import AbstractUser

class CustomerCaptchaStore(CaptchaStore):
    pic_code_seesion_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class FrontUserExtraEmail(AbstractUser, models.Model):
    
    VERIFIED_STATUS_CHOICES = (
        ('0', _('unverified')),
        ('1', _('verified')),
    )
    id = models.AutoField(primary_key=True)
    username = models.EmailField(max_length=255, verbose_name="登录邮箱", null=True, blank=True, help_text="登录邮箱")
    password = models.CharField(max_length=255, verbose_name="登录密码", null=True, blank=True, help_text="密码")
    salt = models.CharField(max_length=255, verbose_name="密码盐值", null=True, blank=True, help_text="密码盐值")
    verified = models.IntegerField(_('Status (*)'), choices=VERIFIED_STATUS_CHOICES, default='0', help_text="是否验证 0 否 1 是")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")
    

    class Meta:
        db_table = "front_user_extra_email"
        verbose_name = "用户邮箱注册表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class EmailVerifyCode(models.Model):
    
    BIZ_TYPE_CHOICES = (
        ('10', _('注册认证')),
        ('11', _('找回密码认证')),
    )
    id = models.AutoField(primary_key=True)
    to_email_address = models.EmailField(max_length=64, verbose_name="验证码接收邮箱", null=True, blank=True, help_text="验证码接收邮箱")
    verify_code = models.CharField(max_length=64, verbose_name="邮箱验证码", null=True, blank=True, help_text="邮箱验证码")
    verify_ip = models.CharField(max_length=128, verbose_name="验证IP", null=True, blank=True, help_text="验证IP")
    expire_at = models.DateTimeField(verbose_name="验证码过期时间", null=True, blank=True, help_text="验证码过期时间")
    biz_type = models.CharField(_('Status (*)'), max_length=2, choices=BIZ_TYPE_CHOICES, default='10', help_text="注册认证")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")

    class Meta:
        db_table = "email_verify_code"
        verbose_name = "邮箱验证码核销记录表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class FrontUserExtraBinding(models.Model):
    
    id = models.AutoField(primary_key=True)
    binding_type = models.CharField(max_length=32, verbose_name="绑定类型,qq,wechat,sina,github,email,phone", null=True, blank=True, default='email', help_text="绑定类型,qq,wechat,sina,github,email,phone")
    extra_info_id = models.IntegerField(verbose_name="额外信息表ID", null=True, blank=True, help_text="额外信息表ID")
    base_user_id = models.IntegerField(verbose_name="基础用户表的ID", null=True, blank=True, help_text="基础用户表的ID")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")

    class Meta:
        db_table = "front_user_extra_binding"
        verbose_name = "前端用户绑定表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class FrontUserBase(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.EmailField(max_length=255, verbose_name="登录邮箱", null=True, blank=True, help_text="登录邮箱")
    nickname = models.CharField(max_length=32, verbose_name="用户昵称", null=True, blank=True, help_text="用户昵称")
    description = models.CharField(max_length=255, verbose_name="描述", null=True, blank=True, help_text="描述")
    avatar_version = models.CharField(max_length=32, verbose_name="头像版本", null=True, blank=True, help_text="头像版本")
    last_login_ip = models.CharField(max_length=128, verbose_name="上一次登录IP", null=True, blank=True, help_text="上一次登录IP")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")

    class Meta:
        db_table = "front_user_base"
        verbose_name = "用户基础信息表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

class SysFrontUserLoginLog(models.Model):
    
    LOGIN_STATUS_CHOICES = (
        ('1', _('登录成功')),
        ('0', _('登录失败')),
    )
    id = models.AutoField(primary_key=True)
    base_user_id = models.IntegerField(verbose_name="登录的基础用户ID", null=True, blank=True, help_text="登录的基础用户ID")
    login_type = models.CharField(max_length=32, verbose_name="登录方式（注册方式）", null=True, blank=True, help_text="登录方式（注册方式）邮箱,手机")
    login_extra_info_id = models.IntegerField(verbose_name="登录信息ID与login_type有关联，邮箱登录时关联front_user_extra_email", null=True, help_text="登录信息ID与login_type有关联，邮箱登录时关联front_user_extra_email")
    login_ip = models.CharField(max_length=32, verbose_name="登录的IP地址", null=True, blank=True, help_text="登录的IP地址")
    login_status = models.CharField(_('Status (*)'), max_length=1, choices=LOGIN_STATUS_CHOICES, default='0', help_text="登录状态，1登录成功，0登录失败")
    message = models.CharField(max_length=64, verbose_name="结果，如果成功一律success；否则保存错误信息", null=True, blank=True, help_text="结果，如果成功一律success；否则保存错误信息")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")


    class Meta:
        db_table = "sys_front_user_login_log"
        verbose_name = "前端用户登录日志表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

class SysEmailSendLog(models.Model):
    
    BIZ_TYPE_CHOICES = (
        ('10', _('注册认证')),
        ('11', _('找回密码认证')),
    )

    SEND_STATUS_CHOICES = (
        ('1', _('发送成功')),
        ('0', _('发送失败')),
    )
    id = models.AutoField(primary_key=True)
    from_email_address = models.EmailField(max_length=64, verbose_name="发件人邮箱", null=True, blank=True, help_text="发件人邮箱")
    to_email_address = models.EmailField(max_length=64, verbose_name="验证码接收邮箱", null=True, blank=True, help_text="验证码接收邮箱")
    biz_type = models.CharField(_('Status (*)'), max_length=2, choices=BIZ_TYPE_CHOICES, default='10', help_text="注册认证")
    request_ip = models.CharField(max_length=32, verbose_name="请求IP", null=True, blank=True, help_text="请求IP")
    content = models.TextField(verbose_name="发送内容", null=True, blank=True, help_text="发送内容")
    message_id = models.CharField(max_length=128, verbose_name="发送后会返回一个messageId", null=True, blank=True, help_text="发送后会返回一个messageId")
    status = models.CharField(_('Status (*)'), max_length=1, choices=SEND_STATUS_CHOICES, default='0', help_text="发送状态，0失败，1成功")
    message = models.CharField(max_length=255, verbose_name="发送后的消息，用于记录成功/失败的信息，成功默认为success", null=True, blank=True, help_text="发送后的消息，用于记录成功/失败的信息，成功默认为success")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")


    class Meta:
        db_table = "sys_email_send_log"
        verbose_name = "邮箱发送日志"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)