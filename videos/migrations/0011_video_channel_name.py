# Generated by Django 5.1.5 on 2025-02-09 03:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0010_alter_video_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="channel_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
