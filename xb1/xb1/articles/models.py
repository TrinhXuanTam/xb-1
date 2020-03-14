from django.db import models

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


class Article(models.Model):

    title = models.CharField("Title", max_length=100)
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.SET_NULL, blank=True, null=True)
    text = models.TextField("Text", blank=True, null=True)
