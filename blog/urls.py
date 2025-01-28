from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, PostSitemap  # Import your sitemaps

sitemaps = {
    "static": StaticViewSitemap,
    "posts": PostSitemap,
}

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("posts/", views.posts, name="posts"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
]
