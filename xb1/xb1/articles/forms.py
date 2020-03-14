from django import forms

from .models import Animal


class AnimalForm(forms.ModelForm):
    """
    TODO - just for testing -will be deleted
    """

    class Meta:
        model = Animal
        fields = ("name", "type", "can_swim", "note")

    def clean(self):

        cleaned_data = super(AnimalForm, self).clean()
        if cleaned_data.get("name") == "dog":
            self.add_error("name", "Name cannot be dog.")

        return cleaned_data
