# Generated by Django 3.2.3 on 2021-05-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videos", "0003_rename_length_video_duration"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="title",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
