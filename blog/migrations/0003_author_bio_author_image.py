# Generated by Django 5.1.4 on 2025-01-26 13:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_post_youtube_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="bio",
            field=models.TextField(
                null=True, validators=[django.core.validators.MinLengthValidator(10)]
            ),
        ),
        migrations.AddField(
            model_name="author",
            name="image",
            field=models.ImageField(null=True, upload_to="authors"),
        ),
    ]
