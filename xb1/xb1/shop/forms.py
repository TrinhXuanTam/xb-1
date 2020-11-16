from django import forms
from django.utils.translation import ugettext_lazy as _

from ..core.widgets import DatePickerInput
from .models import Item

class ItemForm(forms.ModelForm):
    #price = forms.FloatField(label=_("Product price"))
    since = forms.DateTimeField(label=_("Since"))
    till = forms.DateTimeField(label=_("Till"))

    def clean(self):
        return super(ItemForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

        #self.fields['name'].widget.attrs['class'] = 'input_center'
        #self.fields['desc'].widget.attrs['class'] = 'input_center'
        #self.fields['image'].widget.attrs['class'] = 'input_img'
        #self.fields['price'].widget.attrs['class'] = 'input_center'
        #self.fields['since'].widget.attrs['class'] = 'input_center'
        self.fields['since'].widget = DatePickerInput()
        self.fields['till'].widget = DatePickerInput()
        #self.fields['till'].widget.attrs['class'] = 'input_center'

    class Meta:
        model = Item
        fields = ()
        widgets = {
            'image': forms.FileInput
        }