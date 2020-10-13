from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import ShopOrder
from .models import ShopItem

class OrderForm(forms.ModelForm):
	class Meta:
		model = ShopOrder
		fields = ("orderFirstName", "orderLastName", "orderEmail", "orderAddressCity", "orderAddressStreet", "orderAddressPostNumber", "orderPhone", )
		labels = {
			'orderAddressPostNumber': _("Postal code"),
		}
	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)

		for field_name in ("orderFirstName", "orderLastName", "orderEmail", "orderAddressCity", "orderAddressStreet", "orderAddressPostNumber", "orderPhone"):
			self.fields[field_name].widget.attrs['class'] = 'order_form_input'

class ShopItemForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ShopItemForm, self).__init__(*args, **kwargs)

		# set css class
		self.fields['itemActive'].widget.attrs['class'] = 'input_left'
		self.fields['itemType'].widget.attrs['class'] = 'input_left'
		self.fields['itemName'].widget.attrs['class'] = 'input_center'
		self.fields['itemDesc'].widget.attrs['class'] = 'input_center'
		self.fields['itemPrice'].widget.attrs['class'] = 'input_center'
		self.fields['itemImg'].widget.attrs['class'] = 'input_img'
	class Meta:
		model = ShopItem
		fields = ("itemName", "itemDesc", "itemPrice", "itemType", "itemActive", "itemImg")
		widgets = {
			'itemImg': forms.FileInput,
		}
