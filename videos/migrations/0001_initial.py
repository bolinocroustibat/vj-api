# Generated by Django 3.2.2 on 2021-05-13 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Theme",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
            ],
            options={
                "db_table": "themes",
            },
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("youtube_id", models.CharField(max_length=32, unique=True)),
                ("length", models.IntegerField(null=True)),
                ("best_start", models.IntegerField(null=True)),
                (
                    "theme",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="videos.theme"
                    ),
                ),
            ],
            options={
                "db_table": "videos",
            },
        ),
    ]
