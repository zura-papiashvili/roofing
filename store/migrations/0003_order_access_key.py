# Generated by Django 5.1.4 on 2025-01-29 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_order_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="access_key",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
