from django.contrib import admin

from ..core.admin import CustomAdmin
from .models import Item, Price

@admin.register(Item)
class ItemAdmin(CustomAdmin):
	list_display = ("name", "image", "desc", "price", "is_deleted")

@admin.register(Price)
class PriceAdmin(CustomAdmin):
	list_display = ("price", "since", "till", "item", "is_deleted")