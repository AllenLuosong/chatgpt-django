# Generated by Django 4.2.4 on 2024-02-06 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt_image', '0004_alter_imagemessage_number_alter_imagemessage_prompt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemessage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='创建日期', null=True, verbose_name='创建日期'),
        ),
    ]