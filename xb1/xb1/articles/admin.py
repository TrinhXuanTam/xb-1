from django.contrib import admin

from ..core.admin import CustomAdmin
from .models import Article, Category, Tag, Comment, Forum, ForumCategory, UploadedFile


@admin.register(Article)
class ArticleAdmin(CustomAdmin):

    list_display = ("title", "author", "is_deleted", "text")


@admin.register(Category)
class CategoryAdmin(CustomAdmin):

    list_display = ["name", "is_deleted"]


@admin.register(Tag)
class TagAdmin(CustomAdmin):

    list_display = ["name", "is_deleted"]


@admin.register(Forum)
class ForumAdmin(CustomAdmin):

    list_display = ("title", "description", "author", "is_closed", "category", "is_deleted")


@admin.register(ForumCategory)
class ForumAdmin(CustomAdmin):

    list_display = ("title", "is_open", "is_deleted")


@admin.register(Comment)
class ForumAdmin(CustomAdmin):

    list_display = ("article", "forum", "text", "author", "is_censured", "reaction_to", "is_deleted")

@admin.register(UploadedFile)
class UploadedfileAdmin(admin.ModelAdmin):
    pass
