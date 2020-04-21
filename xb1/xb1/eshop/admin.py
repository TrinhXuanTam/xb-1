from django.contrib import admin

from .models import ShopItem
from .models import ShopOrder
from .models import ShopOrderItem

@admin.register(ShopItem)
class ShopItemAdmin(admin.ModelAdmin):
	list_display = ("itemName", "itemPrice", "itemImg", "itemDesc", "itemType", "itemActive")
	
@admin.register(ShopOrder)
class ShopOrderAdmin(admin.ModelAdmin):
	list_display = ("orderFirstName", "orderLastName", "orderEmail", "orderAddressCity", "orderAddressStreet", "orderAddressStreetNumber", "orderAddressPostNumber")
	
@admin.register(ShopOrderItem)
class ShopOrderItem(admin.ModelAdmin):
	list_display = ("shopItem", "shopOrder", "shopItemCount")