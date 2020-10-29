from django.contrib import admin

from ..core.admin import CustomAdmin
from .models import ShopItem, ShopOrder, ShopOrderItem, ShopPayment

@admin.register(ShopItem)
class ShopItemAdmin(CustomAdmin):
	list_display = ("itemName", "itemPrice", "itemImg", "itemDesc", "itemType", "itemActive", "is_deleted")

@admin.register(ShopOrder)
class ShopOrderAdmin(CustomAdmin):
	list_display = ("orderFirstName", "orderLastName", "orderEmail", "orderAddressCity", "orderAddressStreet", "orderAddressPostNumber", "orderPhone", "is_deleted")

@admin.register(ShopOrderItem)
class ShopOrderItemAdmin(CustomAdmin):
	list_display = ("shopItem", "shopOrder", "shopItemCount", "is_deleted")

@admin.register(ShopPayment)
class ShopPaymentAdmin(CustomAdmin):
	list_display = ("paymentPrice", "paymentReceived", "paymentVariableSymbol", "paymentSpecificSymbol", "is_deleted")
