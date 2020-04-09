from django.contrib import admin

from .models import Animal, Article, Category, Tag, Comment, Forum, ForumCategory


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    
    list_display = ("name", "note", "type", "can_swim")


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

    list_display = ("article", "forum", "reaction_to", "author", "text", "is_censured")
