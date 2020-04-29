from django import forms

from .models import ShopOrder
from .models import ShopItem

class OrderForm(forms.ModelForm):
	class Meta:
		model = ShopOrder
		fields = ("orderFirstName", "orderLastName", "orderEmail", "orderAddressCity", "orderAddressStreet", "orderAddressStreetNumber", "orderAddressPostNumber")

class ShopItemForm(forms.ModelForm):
	class Meta:
		model = ShopItem
		fields = ("itemName", "itemPrice", "itemImg", "itemDesc", "itemType", "itemActive")