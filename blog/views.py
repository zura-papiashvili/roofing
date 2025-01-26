from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render

from .models import Author, Post


def home(request):
    posts = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/home.html", {"posts": posts})


def about(request):
    authors = Author.objects.all()
    return render(request, "about.html", {"authors": authors})


def contact(request):
    return render(request, "contact.html")


def posts(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, "blog/posts.html", {"posts": posts})
