# Generated by Django 5.1.2 on 2025-02-22 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix_app', '0006_rename_created_by_video_uploaded_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='author',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
    ]
