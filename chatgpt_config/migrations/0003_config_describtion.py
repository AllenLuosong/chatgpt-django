# Generated by Django 4.2.4 on 2024-01-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt_config', '0002_alter_config_key_alter_config_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='describtion',
            field=models.CharField(blank=True, help_text='描述', max_length=255, null=True, verbose_name='描述'),
        ),
    ]