# Generated by Django 4.2.4 on 2023-09-12 21:25

import chatgpt_image.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt_image', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, help_text='名称', max_length=200, null=True, verbose_name='名称')),
                ('url', models.FileField(upload_to=chatgpt_image.models.media_file_name)),
                ('md5sum', models.CharField(blank=True, help_text='文件md5', max_length=36, verbose_name='文件md5')),
                ('update_datetime', models.DateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '文件管理',
                'verbose_name_plural': '文件管理',
                'db_table': 'Image_file',
                'ordering': ('-create_datetime',),
            },
        ),
    ]
