# Generated by Django 3.2.3 on 2021-05-17 05:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0004_video_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="thumbnail",
            field=models.URLField(null=True),
        ),
    ]
