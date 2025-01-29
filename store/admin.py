from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Category, Variation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "discount_percentage",
        "stock",
        "created_at",
    )
    search_fields = ("name", "category__name")
    list_filter = ("category", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "name", "price_adjustment", "stock")
    search_fields = ("product__name", "name")
    list_filter = ("product",)
