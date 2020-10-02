from django import forms

import django.utils.formats

from .models import Article, Comment, Category, Tag
from ..core.widgets import DateTimePickerInput
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms.widgets import CheckboxSelectMultiple

class ArticleForm(forms.ModelForm):

    class Meta:
        forms.DateTimeField
        model = Article
        fields = [
            "title", "thumbnail","preview_text" , "text", "slug", "category",
            "tags", "allow_comments", "sources", "article_state", "published_from",
            "published_to"
        ]

    def __init__(self, *args, **kwargs):

        super(ArticleForm, self).__init__(*args, **kwargs)

        self.fields["published_from"].widget = DateTimePickerInput()
        self.fields["published_from"].widget.attrs["autocomplete"] = "off"

        self.fields["published_to"].widget = DateTimePickerInput()
        self.fields["published_to"].widget.attrs["autocomplete"] = "off"

        self.fields["text"].widget = CKEditorUploadingWidget()

        self.fields["category"].widget = CheckboxSelectMultiple()
        self.fields["category"].queryset = Category.objects.all()

    def clean(self):

        cleaned_data = super(ArticleForm, self ).clean()

        print(cleaned_data)

        return cleaned_data
