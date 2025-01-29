# Generated by Django 5.1.4 on 2025-01-29 18:24

import blog.utils
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=255)),
                ("color", models.CharField(blank=True, max_length=255, null=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "discount_percentage",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="store/product_images/",
                        validators=[blog.utils.validate_image_size],
                    ),
                ),
                ("stock", models.PositiveIntegerField(default=0)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="store.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Variation",
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
                ("name", models.CharField(max_length=255)),
                (
                    "price_adjustment",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                ("stock", models.PositiveIntegerField(default=0)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variations",
                        to="store.product",
                    ),
                ),
            ],
        ),
    ]
