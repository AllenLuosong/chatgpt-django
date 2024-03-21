# Generated by Django 4.2.4 on 2024-03-03 20:17

import chatgpt_config.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt_config', '0019_rename_content_userconfig_chatmodellist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconfig',
            name='chatModelList',
            field=models.JSONField(default=chatgpt_config.models.get_chatModel_list, verbose_name='权限列表'),
        ),
    ]