from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from PIL import Image

class MyUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    # new email when users change email, temp will be set to email if users authenticate their new email
    temp_email = models.EmailField(null=True)
    signup_confirmation = models.BooleanField(default=False)
    objects = MyUserManager()

    class Meta:
        permissions = (
            ("is_staff_user", "Is user a staff"),
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), default='default.jpg', blank=True, null=True, upload_to='profile_image')
    nickname = models.CharField(_('Nickname'), unique=True, max_length=30, null=True, blank=True)
    city = models.CharField(_("City"), max_length=100, null=True, blank=True)
    postalCode = models.CharField(_("Postal Code"), max_length=10, null=True, blank=True)
    address = models.CharField(_("Address"), max_length=100, null=True, blank=True)
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True)
    surname = models.CharField(_("Surname"), max_length=100, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.user}\'s profile'

    def save(self, *args, **kwargs):
        """
        When a profile is modified, function checks parameters of profile image and downsizes it if it is too big
        """
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
            else:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
