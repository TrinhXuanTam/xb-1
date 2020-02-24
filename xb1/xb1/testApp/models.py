from django.db import models


class Animal(models.Model):

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
