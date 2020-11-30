from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from ..core.widgets import DatePickerInput
from .models import Item, Order

class ItemCreateForm(forms.ModelForm):
    price = forms.FloatField(label=_("Product price"))
    till = forms.DateTimeField(label=_("Till"))
    specificationname = forms.CharField(label=_("Specification name"), max_length = 50,required=False)
    specificationvalue = forms.CharField(label=_("Specification value"), max_length = 50,required=False)

    def __init__(self, *args, **kwargs):
        super(ItemCreateForm, self).__init__(*args, **kwargs)
        self.fields['till'].widget = DatePickerInput(attrs={'autocomplete':'off'})

    class Meta:
        model = Item
        fields = ("name", "desc", "image")
        widgets = {
            'image': forms.FileInput
        }

class ItemUpdateForm(forms.ModelForm):
    price = forms.FloatField(label=_("Product price"))
    till = forms.DateTimeField(label=_("Till"))
    specificationname = forms.CharField(label=_("Specification name"), max_length = 50,required=False)
    specificationvalue = forms.CharField(label=_("Specification value"), max_length = 50,required=False)

    def clean(self):
        return super(ItemUpdateForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(ItemUpdateForm, self).__init__(*args, **kwargs)
        self.fields['till'].widget = DatePickerInput(attrs={'autocomplete':'off'})

    class Meta:
        model = Item
        fields = ("name", "desc", "image")
        widgets = {
            'image': forms.FileInput
        }

class OrderCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        for field_name in ("firstname", "lastname", "email", "city", "street", "post", "phone"):
            self.fields[field_name].widget.attrs['class'] = 'order_form_input'

    def clean(self):

        cleaned_data = super(OrderCreateForm, self).clean()
        
        for field_name in ("firstname", "lastname", "email", "city", "street", "post", "phone"):
            if not cleaned_data[field_name]:
                self.add_error(field_name, _("Empty value is not allowed"))
                self.fields[field_name].widget.attrs['style'] = 'border-color: red'

        return cleaned_data

    class Meta:
        model = Order
        fields = ("firstname", "lastname", "email", "city", "street", "post", "phone")
        labels = {
            'post': _("Postal code"),
        }