from django import forms

from .models import ShopOrder

class OrderForm(forms.ModelForm):
	class Meta:
		model = ShopOrder
		fields = ("orderFirstName", "orderLastName", "orderEmail", "orderAddressCity", "orderAddressStreet", "orderAddressStreetNumber", "orderAddressPostNumber")
