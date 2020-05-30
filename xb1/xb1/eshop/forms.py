from django import forms

from .models import ShopOrder
from .models import ShopItem

class OrderForm(forms.ModelForm):
	class Meta:
		model = ShopOrder
		fields = ("orderFirstName", "orderLastName", "orderEmail", "orderAddressCity", "orderAddressStreet", "orderAddressPostNumber", "orderPhone", )
		labels = {
			'orderAddressPostNumber': "PSČ",
		}
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
