from django.db import models
from model_utils.models import TimeStampedModel
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

from ..core.models import User


class Category(models.Model):

    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name


# TimeStampedModel - An abstract base class model that provides self-updating "created" and "modified" fields.
class Article(TimeStampedModel):
    """
    TODO: Update: text field formatting
    Create: thumbnail fields
    """

    HIDDEN = 0
    PUBLISHED = 1
    STATE_CHOICES = (
        (HIDDEN, _("Hidden")),
        (PUBLISHED, _("Published"))
    )

    title          = models.CharField(verbose_name=_("Title"), max_length=100)
    thumbnail      = models.ImageField(verbose_name=_("Thumbnail"), null=True, blank=True, upload_to='thumbnails')
    author         = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.SET_NULL, blank=True, null=True)
    slug           = models.SlugField(verbose_name=_("Slug"), unique=True, max_length=100, blank=True, null=True)
    category       = models.ManyToManyField(Category, verbose_name=_("Category"), blank=True)
    tags           = models.ManyToManyField(Tag, verbose_name=_("Tag"), blank=True)
    allow_comments = models.BooleanField(verbose_name=_("Comments allowed"), default=False)
    published_from = models.DateTimeField(verbose_name=_("Published from"), default=datetime.now, null=True, blank=True)
    published_to   = models.DateTimeField(verbose_name=_("Published to"), null=True, blank=True)
    text           = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    sources        = models.TextField(verbose_name=_("Sources"), blank=True, null=True)
    article_state  = models.PositiveSmallIntegerField(verbose_name=_("State"), choices=STATE_CHOICES, default=HIDDEN)


class ForumCategory(models.Model):

    title = models.CharField(verbose_name=_("Title"), max_length=100)
    is_open = models.BooleanField(verbose_name=_("Is public"), default=True)

    def __str__(self):
        return self.title


class Forum(TimeStampedModel):

    title = models.CharField(verbose_name=_("Title"), max_length=100)
    description = models.TextField(verbose_name=_("Forum description"), blank=True, null=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.SET_NULL, blank=True, null=True)
    is_closed = models.BooleanField(verbose_name=_("Is closed"), default=False)
    category = models.ForeignKey(ForumCategory, verbose_name=_("Category"), on_delete=models.SET_NULL, blank=True, null=True)


class Comment(TimeStampedModel):

    article = models.ForeignKey(Article, verbose_name=_("Article"), on_delete=models.CASCADE, blank=True, null=True)
    forum = models.ForeignKey(Forum, verbose_name=_("Forum"), on_delete=models.CASCADE, blank=True, null=True)
    reaction_to = models.ForeignKey("Comment", verbose_name=_("Reacts to"), on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField(verbose_name=_("Text"), blank=True, null=True)
    is_censured = models.BooleanField(verbose_name=_("Is censured"), default=False)

