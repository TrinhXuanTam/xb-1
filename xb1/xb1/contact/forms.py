from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    message = forms.CharField(label=_("Message"), max_length=2000, required=True, widget=forms.Textarea(
        attrs={"placeholder": _("Your message..."), "class": "form-control", "rows": 11}))
    subject = forms.CharField(label=_("Subject"), max_length=100, required=True, widget=forms.TextInput(
        attrs={"placeholder": _("Subject...")}))
    #   name = forms.CharField(label="Name", max_length=100, required=True, widget=forms.TextInput(
    #     attrs={"placeholder":"Jméno..."}))
    captcha = CaptchaField()

