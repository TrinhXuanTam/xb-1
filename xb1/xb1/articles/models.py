from django.db import models
from model_utils.models import TimeStampedModel
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from os.path import basename, splitext
from django.utils.text import slugify


from ..core.models import User

import random

class Category(models.Model):
    """
    Category model for filtering articles.
    """

    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Category tags model for filtering articles.
    """

    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    """
    CKEditor model for storing uploaded files.
    """

    uploaded_file = models.FileField(upload_to=u"article_content_images/")
    uploaded_at = models.DateField(editable=False, auto_now_add=True)

    def __str__(self):
        return basename(self.uploaded_file.path)

    def url(self):
        return self.uploaded_file.url

    def delete(self, *args, **kwargs):
        file_storage, file_path = self.uploaded_file.storage, self.uploaded_file.path
        super(UploadedFile, self).delete(*args, **kwargs)
        name, ext = splitext(file_path)
        file_storage.delete(file_path)
        file_storage.delete(name + "_thumb" + ext)

class Article(TimeStampedModel):

    HIDDEN = 0
    PUBLISHED = 1
    STATE_CHOICES = (
        (HIDDEN, _("Hidden")),
        (PUBLISHED, _("Published"))
    )

    title          = models.CharField(verbose_name=_("Title"), max_length=100)
    thumbnail      = models.ImageField(verbose_name=_("Thumbnail"), null=True, blank=True, upload_to='thumbnails')
    preview_text   = models.TextField(verbose_name=_("Preview text"), blank=True, null=False, default=_("Read more..."))
    author         = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.SET_NULL, blank=True, null=True)
    slug           = models.SlugField(verbose_name=_("Slug"), unique=True, max_length=100, blank=True, null=True)
    category       = models.ManyToManyField(Category, verbose_name=_("Category"), blank=True)
    tags           = models.ManyToManyField(Tag, verbose_name=_("Tag"), blank=True)
    allow_comments = models.BooleanField(verbose_name=_("Comments allowed"), default=False)
    published_from = models.DateTimeField(verbose_name=_("Published from"), default=timezone.now, null=True, blank=True)
    published_to   = models.DateTimeField(verbose_name=_("Published to"), null=True, blank=True)
    text           = RichTextField(verbose_name=_("Text"), blank=True, null=True)
    sources        = models.TextField(verbose_name=_("Sources"), blank=True, null=True)
    article_state  = models.PositiveSmallIntegerField(verbose_name=_("State"), choices=STATE_CHOICES, default=HIDDEN)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self._generate_slug()

        super().save(*args, **kwargs)

    def _generate_slug(self):

        slg = slugify(self.title)

        # Test if slug exists
        while Article.objects.filter(slug=slg).exists():
            slg = slg + "_" + str(random.randint(0, 1000))

        self.slug = slg


class ForumCategory(models.Model):

    title = models.CharField(verbose_name=_("Title"), max_length=100)
    is_open = models.BooleanField(verbose_name=_("Is public"), default=True)
    description = models.TextField(verbose_name=_("Popis tématu"), blank=True, null=True)

    def __str__(self):
        return self.title


class Forum(TimeStampedModel):

    title = models.CharField(verbose_name=_("Title"), max_length=100)
    description = models.TextField(verbose_name=_("Popis vlákna"), blank=True, null=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.SET_NULL, blank=True, null=True)
    is_closed = models.BooleanField(verbose_name=_("Is closed"), default=False)
    category = models.ForeignKey(ForumCategory, verbose_name=_("Category"), on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):

    article = models.ForeignKey(Article, verbose_name=_("Article"), on_delete=models.CASCADE, blank=True, null=True)
    forum = models.ForeignKey(Forum, verbose_name=_("Forum"), on_delete=models.CASCADE, blank=True, null=True)
    reaction_to = models.ForeignKey("Comment", verbose_name=_("Reacts to"), on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.SET_NULL, blank=True, null=True)
    text = RichTextField(verbose_name=_("Text"), blank=True, null=True, config_name="comment")
    is_censured = models.BooleanField(verbose_name=_("Is censured"), default=False)
    date = models.DateTimeField(verbose_name=_("Posted on"), default=timezone.now, null=False, blank=False, editable=False)

    def __str__(self):
        return self.text if self.text else "---"
