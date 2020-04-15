from django import forms

from .models import Animal, Article
from ..core.widgets import DateTimePickerInput


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


class ArticleForm(forms.ModelForm):

    class Meta:
        forms.DateTimeField
        model = Article
        fields = [
            "title", "thumbnail", "text", "slug", "category", "tags",
            "allow_comments", "sources", "article_state", "published_from",
            "published_to"
        ]
    
    def __init__(self, *args, **kwargs):

        super(ArticleForm, self).__init__(*args, **kwargs)

        self.fields["published_from"].widget = DateTimePickerInput()
        self.fields["published_from"].widget.attrs["input_formats"] = ['%d/%m/%Y %H:%M']

        self.fields["published_to"].widget = DateTimePickerInput()
        self.fields["published_to"].widget.attrs["input_formats"] = ['%d/%m/%Y %H:%M']
