from django import forms


class ContactForm(forms.Form):
    message = forms.CharField(label="Message", max_length=2000, required=True, widget=forms.Textarea(
        attrs={"placeholder": "Vaše zpráva...", "class": "form-control", "rows": 5}))
    topic = forms.CharField(label="Topic", max_length=100, required=True, widget=forms.TextInput(
        attrs={"placeholder": "Předmět..."}))
    name = forms.CharField(label="Name", max_length=100, required=True, widget=forms.TextInput(
        attrs={"placeholder":"Jméno..."}))
