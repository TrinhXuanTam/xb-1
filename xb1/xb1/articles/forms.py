from django import forms

import django.utils.formats

from .models import Article
from ..core.widgets import DateTimePickerInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget


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
        self.fields["published_from"].widget.attrs["autocomplete"] = "off"

        self.fields["published_to"].widget = DateTimePickerInput()
        self.fields["published_to"].widget.attrs["autocomplete"] = "off"
        
        self.fields["text"].widget = CKEditorUploadingWidget()

    def clean(self):

        cleaned_data = super(ArticleForm, self ).clean()

        print(cleaned_data)

        return cleaned_data