from django.contrib import admin

from ..core.admin import CustomAdmin
from .models import Item, Price, CartEntry, Cart, Specification, SpecificationEntry, Order, Payment

@admin.register(Item)
class ItemAdmin(CustomAdmin):
	list_display = ("name", "image", "desc", "price", "is_deleted")

@admin.register(Price)
class PriceAdmin(CustomAdmin):
	list_display = ("price", "since", "till", "item", "is_deleted")

@admin.register(CartEntry)
class CartEntryAdmin(CustomAdmin):
	list_display = ("count", "price", "item", "cart", "is_deleted")

@admin.register(Cart)
class CartAdmin(CustomAdmin):
	list_display = ("creation", "order", "is_deleted")

@admin.register(Specification)
class SpecificationAdmin(CustomAdmin):
	list_display = ("name", "item", "active", "is_deleted")

@admin.register(SpecificationEntry)
class SpecificationAdmin(CustomAdmin):
	list_display = ("value", "specification", "is_deleted")
	
@admin.register(Order)
class OrderAdmin(CustomAdmin):
	list_display = ("firstname", "lastname", "email", "phone", "is_deleted")

@admin.register(Payment)
class PaymentAdmin(CustomAdmin):
	list_display = ("received", "variableSymbol", "specificSymbol", "order", "is_deleted")