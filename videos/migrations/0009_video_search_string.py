# Generated by Django 3.2.7 on 2021-09-16 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_auto_20210916_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='search_string',
            field=models.CharField(editable=False, max_length=255, null=True),
        ),
    ]
