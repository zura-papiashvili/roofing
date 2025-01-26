from django.contrib import admin

# Register your models here.

from .models import Author, Tag, Post, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email_address")
    search_fields = ("last_name", "first_name")


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "author")
    list_filter = ("author", "date", "tags")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post", "text")
    search_fields = ("user_name", "text")


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
