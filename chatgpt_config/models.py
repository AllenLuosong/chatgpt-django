from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
# VIP_TYPE = models.IntegerField(verbose_name="用户类型", choices=VIP_TYPE_CHOICES, default=0, help_text="用户类型")

class Config(models.Model):
        
    config_Code_CHOICES = (
        # 业务配置码枚举值
        ('openai_chat_api_3_5', _('3.5会话配置项')),
        ('openai_chat_api_4', _('4.0会话配置项')),
        ('openai_image_api_DALL_E_2', _('Dall2绘图配置项')),
        ('openai_image_api_DALL_E_3', _('Dall3绘图配置项')),
        ('email_config', _('邮箱服务器配置项')),
    )
    id = models.AutoField(primary_key=True)
    config_Code = models.CharField(max_length=64, choices=config_Code_CHOICES, default=10, verbose_name="业务配置码", null=True, blank=True, help_text="业务配置码")
    key = models.CharField(max_length=64, verbose_name="配置键", null=True, blank=True, help_text="配置键")
    value = models.CharField(max_length=255, verbose_name="配置值", null=True, blank=True, help_text="配置值")
    describtion = models.CharField(max_length=255, verbose_name="描述", null=True, blank=True, help_text="描述")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")

    class Meta:
        db_table = "chatgpt_config"
        verbose_name = "业务配置表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    # def __str__(self) -> str:
    #     return self.id, self.config_Code
    
class UserConfig(models.Model):
    id = models.AutoField(primary_key=True)
    baseUserId = models.IntegerField(verbose_name="用户ID", null=True, blank=True, help_text="用户ID")
    secretKey = models.CharField(max_length=64, verbose_name="配置键", null=True, blank=False, help_text="配置键")
    proxyAdress = models.CharField(max_length=255, verbose_name="配置值", null=True, blank=False, help_text="配置值")
    chatModel = models.CharField(max_length=255, verbose_name="描述", null=True, blank=False, help_text="描述")
    drawvalue = models.CharField(max_length=255, verbose_name="描述", null=True, blank=False, help_text="描述")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")

    class Meta:
        db_table = "user_config"
        verbose_name = "用户配置表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)
