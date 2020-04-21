from django.contrib import admin

from .models import ShopItem
from .models import ShopOrder

@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
	list_display = ("itemName", "itemPrice", "itemDesc", "itemType", "itemActive")
	
@admin.register(ShopOrder)
class ShopItemAdmin(admin.ModelAdmin):
	list_display = ("orderFirstName", "orderLastName", "orderEmail", "orderAddressCity", "orderAddressStreet", "orderAddressStreetNumber", "orderAddressPostNumber")