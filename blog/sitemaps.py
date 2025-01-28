from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post  # Replace with your model


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ["home", "about", "contact"]  # Add the names of your static views

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return Post.objects.all()  # Replace with your model to list dynamic URLs

    def lastmod(self, obj):
        return obj.updated_at  # Use the field from your model that tracks updates
