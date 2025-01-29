from django.db import models
from blog.utils import validate_image_size, compress_and_optimize_image
from django.utils.text import slugify
import hashlib


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


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")
    access_key = models.CharField(max_length=255, unique=True, blank=True)

    # Customer Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    shipping_address = models.TextField()
    access_key = models.CharField(max_length=255, blank=True)

    def generate_access_key(self):
        """Generate a consistent access key based on the user's email."""
        # Create a hash of the user's email (or user ID) for the access key
        return hashlib.sha256(self.email.encode("utf-8")).hexdigest()

    def save(self, *args, **kwargs):
        """Override save to set access key."""
        if not self.access_key:
            self.access_key = self.generate_access_key()
        print(f"Saving order with access_key: {self.access_key}")  # Debugging line

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
