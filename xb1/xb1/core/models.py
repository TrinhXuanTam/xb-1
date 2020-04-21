from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from PIL import Image


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    signup_confirmation = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), default='default.jpg', upload_to='profile_image')
    city = models.CharField(_("City"), max_length=100, null=True, blank=True)
    postalCode = models.CharField(_("PostalCode"), max_length=10, null=True, blank=True)
    address = models.CharField(_("Address"), max_length=100, null=True, blank=True)
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True)
    surname = models.CharField(_("Surname"), max_length=100, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.user}\'s profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        else:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

