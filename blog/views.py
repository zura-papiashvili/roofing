from django.shortcuts import render
from .models import Author, Post, FAQ
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from luzysonido.settings import EMAIL_HOST_USER


def home(request):
    posts = Post.objects.all().order_by("-date")[:3]
    faqs = FAQ.objects.all()
    return render(request, "blog/home.html", {"posts": posts, "faqs": faqs})


def about(request):
    authors = Author.objects.all()
    return render(request, "about.html", {"authors": authors})


# def contact(request):
#     return render(request, "contact.html")


def posts(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, "blog/posts.html", {"posts": posts})


def contact(request):
    if request.method == "POST":
        message_name = request.POST["message-name"]
        message_email = request.POST["message-email"]
        message = request.POST["message"]

        # Create a nicely formatted HTML message
        email_message = render_to_string(
            "email/contact_email.html",  # Create a new template for email content
            {
                "message_name": message_name,
                "message_email": message_email,
                "message": message,
            },
        )

        send_mail(
            f"Message from {message_name}",  # Subject
            "",  # No plain text message
            message_email,  # From email
            [settings.EMAIL_HOST_USER],  # To email
            html_message=email_message,  # HTML message content
        )

        return render(request, "contact.html", {"message_name": message_name})

    return render(request, "contact.html", {})
