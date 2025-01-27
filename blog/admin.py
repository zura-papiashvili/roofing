from django.contrib import admin

# Register your models here.

from .models import Author, Tag, Post, Comment, FAQ


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email_address")
    search_fields = ("last_name", "first_name")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "author")
    list_filter = ("author", "date", "tags")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post", "text")
    search_fields = ("user_name", "text")


class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "answer")
    search_fields = ("question", "answer")


admin.site.register(FAQ, FAQAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
