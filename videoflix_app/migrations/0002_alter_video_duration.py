# Generated by Django 5.1.2 on 2025-03-10 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
