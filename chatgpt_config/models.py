from django.db import models

# Create your models here.
class Config(models.Model):
    id = models.AutoField(primary_key=True)
    config_Code = models.CharField(max_length=64, verbose_name="业务配置码", null=True, blank=True, help_text="业务配置码")
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
