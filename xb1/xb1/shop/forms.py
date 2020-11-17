from django import forms
from django.utils.translation import ugettext_lazy as _

from ..core.widgets import DatePickerInput
from .models import Item

class ItemCreateForm(forms.ModelForm):
    price = forms.FloatField(label=_("Product price"))
    till = forms.DateTimeField(label=_("Till"))
    specificationname = forms.CharField(label=_("Specification name"), max_length = 50,required=False)
    specificationvalue = forms.CharField(label=_("Specification value"), max_length = 50,required=False)

    def clean(self):
        return super(ItemCreateForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(ItemCreateForm, self).__init__(*args, **kwargs)
        self.fields['till'].widget = DatePickerInput()

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
        self.fields['till'].widget = DatePickerInput()

    class Meta:
        model = Item
        fields = ("name", "desc", "image")
        widgets = {
            'image': forms.FileInput
        }