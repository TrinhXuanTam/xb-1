from django.contrib import admin

from .models import Animal, Article, Category, Tag


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