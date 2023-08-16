from django.db import models

# Create your models here.


class ChatMessage(models.Model):
    

    id = models.AutoField(primary_key=True)
    username = models.EmailField(max_length=64, verbose_name="用户名", null=True, blank=True, help_text="用户名")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")

    class Meta:
        db_table = "chat_message"
        verbose_name = "聊天消息表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)