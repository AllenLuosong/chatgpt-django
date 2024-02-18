# Generated by Django 4.2.4 on 2024-02-18 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt_config', '0009_alter_config_config_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userconfig',
            name='chatModel',
            field=models.CharField(help_text='对话模型', max_length=255, null=True, verbose_name='对话模型'),
        ),
        migrations.AlterField(
            model_name='userconfig',
            name='drawvalue',
            field=models.CharField(help_text='绘画模型', max_length=255, null=True, verbose_name='绘画模型'),
        ),
    ]