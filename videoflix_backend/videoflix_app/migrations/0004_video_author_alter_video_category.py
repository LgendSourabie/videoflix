# Generated by Django 5.1.2 on 2025-02-06 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix_app', '0003_alter_video_category_alter_video_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='author',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.CharField(blank=True, choices=[('documentary', 'documentary'), ('action', 'action'), ('horror', 'horror'), ('drama', 'drama'), ('romance', 'romance')], max_length=100, null=True),
        ),
    ]
