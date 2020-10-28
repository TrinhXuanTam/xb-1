from django import forms

import django.utils.formats

from .models import Article, Comment, Category, Tag
from ..core.widgets import DatePickerInput
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

        self.fields["published_from"].widget = DatePickerInput()
        self.fields["published_from"].widget.attrs["autocomplete"] = "off"

        self.fields["published_to"].widget = DatePickerInput()
        self.fields["published_to"].widget.attrs["autocomplete"] = "off"

        self.fields["text"].widget = CKEditorUploadingWidget()

        self.fields["category"].widget = CheckboxSelectMultiple()
        self.fields["category"].queryset = Category.objects.all()

    def clean(self):

        cleaned_data = super(ArticleForm, self ).clean()

        return cleaned_data
