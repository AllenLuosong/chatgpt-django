# Generated by Django 4.2.4 on 2024-02-17 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt_image', '0007_imagemessage_draw_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemessage',
            name='image_quality',
            field=models.CharField(blank=True, help_text='图像质量', max_length=16, null=True, verbose_name='图像质量'),
        ),
    ]