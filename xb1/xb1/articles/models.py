from django.db import models
from model_utils.models import TimeStampedModel
from datetime import datetime
from ..core.models import User


class Animal(models.Model):
    """
    TODO - just for testing -will be deleted
    """

    MAMMAL = 0
    FISH = 1
    ANT = 2

    TYPE_CHOICES = (
        (MAMMAL, "Mammal"),
        (FISH, "Fish"),
        (ANT, "Ant")
    )

    name = models.CharField("Animal name", max_length=50)
    type = models.PositiveSmallIntegerField("Animal type", choices=TYPE_CHOICES)
    can_swim = models.BooleanField("Can swim", default=False)
    note = models.TextField("Note", blank=True, null=True)

    def get_type_display(self):

        return Animal.TYPE_CHOICES[self.type][1]


class Category(models.Model):

    name = models.CharField("Name", max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField("Name", max_length=100)

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
        (HIDDEN, "Hidden"),
        (PUBLISHED, "Published")
    )

    title          = models.CharField("Title", max_length=100)
    author         = models.ForeignKey(User, verbose_name="Author", on_delete=models.SET_NULL, blank=True, null=True)
    slug           = models.SlugField(verbose_name="Slug", unique=True, max_length=100, blank=True, null=True)
    category       = models.ManyToManyField(Category, blank=True)
    tags           = models.ManyToManyField(Tag, blank=True)
    allow_comments = models.BooleanField(verbose_name="Comments allowed", default=False)
    published_from = models.DateTimeField(verbose_name="Published from", default=datetime.now, null=True, blank=True)
    published_to   = models.DateTimeField(verbose_name="Published to", null=True, blank=True)
    text           = models.TextField("Text", blank=True, null=True)
    sources        = models.TextField("Sources", blank=True, null=True)
    article_state  = models.PositiveSmallIntegerField("State", choices=STATE_CHOICES, default=HIDDEN)
