from django.db import models
from blog.utils import validate_image_size, compress_and_optimize_image
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    color = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )  # Discount (0 - 100%)
    image = models.ImageField(
        upload_to="store/product_images/",
        blank=True,
        null=True,
        validators=[validate_image_size],
    )
    stock = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.discount_percentage < 0 or self.discount_percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        super().save(*args, **kwargs)

    def final_price(self):
        """Calculate price after discount"""
        return self.price * (1 - self.discount_percentage / 100)


class Variation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variations"
    )
    name = models.CharField(
        max_length=255
    )  # Example: "1.5mm Thickness", "Aluminum", etc.
    price_adjustment = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def final_price(self):
        """Calculate variation price after discount"""
        return (self.product.price + self.price_adjustment) * (
            1 - self.product.discount_percentage / 100
        )
