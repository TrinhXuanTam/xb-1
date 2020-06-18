from django.contrib import admin

from .models import Article, Category, Tag, Comment, Forum, ForumCategory, UploadedFile


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ("title", "author", "text")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ["name"]


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):

    list_display = ("title", "description", "author", "is_closed", "category")


@admin.register(ForumCategory)
class ForumAdmin(admin.ModelAdmin):

    list_display = ("title", "is_open")


@admin.register(Comment)
class ForumAdmin(admin.ModelAdmin):

    list_display = ("article", "forum", "text", "author", "is_censured", "reaction_to")

@admin.register(UploadedFile)
class UploadedfileAdmin(admin.ModelAdmin):
    pass
