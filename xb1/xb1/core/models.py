from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache

from datetime import datetime
from PIL import Image


class MyUserManager(BaseUserManager):

    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

    def create_user(self, email, username, password=None, is_active=True, is_staff=False, is_superuser=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        user.set_password(password)
        user.save(using=self._db)

        # Automatically create user profile
        profile = Profile()
        profile.user = user
        profile.nickname = user.username
        profile.save()

        return user

    def create_staffuser(self, username, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username
        )
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

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


class Log(models.Model):

    user = models.ForeignKey(User, verbose_name=_("User"), blank=False, null=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True, null=True, blank=True)
    action = models.CharField(_("Action"), max_length=100, null=True, blank=True)

    article = models.ForeignKey("articles.Article", verbose_name=_("Article"), blank=True, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey("articles.Comment", verbose_name=_("Comment"), blank=True, null=True, on_delete=models.CASCADE)
    forum = models.ForeignKey("articles.Forum", verbose_name=_("Forum"), blank=True, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey("shop.Order", verbose_name=_("Order"), blank=True, null=True, on_delete=models.CASCADE)

    @staticmethod
    def user_login(user):

        log = Log(
            user=user,
            action=_("user logged in")
        )
        log.save()
        return log

    @staticmethod
    def user_invalid_login(user):

        log = Log(
            user=user,
            action=_("user failed to log in")
        )
        log.save()
        return log

    @staticmethod
    def user_sent_password_reset_request(user):

        log = Log(
            user=user,
            action=_("user sent password reset request")
        )
        log.save()
        return log

    @staticmethod
    def user_changed_password_via_email(user):

        log = Log(
            user=user,
            action=_("user changed password via email")
        )
        log.save()
        return log

    @staticmethod
    def user_registered(user):

        log = Log(
            user=user,
            action=_("user registered a new account")
        )
        log.save()
        return log

    @staticmethod
    def user_changed_password(user):

        log = Log(
            user=user,
            action=_("user changed a password")
        )
        log.save()
        return log

    @staticmethod
    def user_verified(user):

        log = Log(
            user=user,
            action=_("user verified the account")
        )
        log.save()
        return log

    @staticmethod
    def user_created_article(user, article):

        log = Log(
            user=user,
            action=_("user created new article"),
            article=article
        )
        log.save()
        return log

    @staticmethod
    def user_modified_article(user, article):

        log = Log(
            user=user,
            action=_("user modified article"),
            article=article
        )
        log.save()
        return log

    @staticmethod
    def user_published_article(user, article):

        log = Log(
            user=user,
            action=_("user published article"),
            article=article
        )
        log.save()
        return log

    @staticmethod
    def user_hide_article(user, article):

        log = Log(
            user=user,
            action=_("user hide article"),
            article=article
        )
        log.save()
        return log

    @staticmethod
    def user_deleted_article(user, article):

        log = Log(
            user=user,
            action=_("user deleted article"),
            article=article
        )
        log.save()
        return log

    @staticmethod
    def user_posted_comment(user, comment):

        log = Log(
            user=user,
            action=_("user posted comment"),
            comment=comment
        )
        log.save()
        return log

    @staticmethod
    def user_banned_comment(user, comment):

        log = Log(
            user=user,
            action=_("user banned comment"),
            comment=comment
        )
        log.save()
        return log

    @staticmethod
    def user_unbanned_comment(user, comment):

        log = Log(
            user=user,
            action=_("user unbanned comment"),
            comment=comment
        )
        log.save()
        return log

    @staticmethod
    def user_created_order(user, order):

        log = Log(
            user=user,
            action=_("user created order"),
            order=order
        )
        log.save()
        return log

    @staticmethod
    def user_marked_order_as_paid(user, order):

        log = Log(
            user=user,
            action=_("user marked order as paid"),
            order=order
        )
        log.save()
        return log

    @staticmethod
    def user_marked_order_as_unpaid(user, order):

        log = Log(
            user=user,
            action=_("user marked order as unpaid"),
            order=order
        )
        log.save()
        return log

    @staticmethod
    def user_deleted_order(user, order):

        log = Log(
            user=user,
            action=_("user deleted order"),
            order=order
        )
        log.save()
        return log

    @staticmethod
    def user_created_forum(user, forum):

        log = Log(
            user=user,
            action=_("user created forum"),
            forum=forum
        )
        log.save()
        return log

    @staticmethod
    def user_modified_forum(user, forum):

        log = Log(
            user=user,
            action=_("user modified forum"),
            forum=forum
        )
        log.save()
        return log

    @staticmethod
    def user_deleted_forum(user, forum):

        log = Log(
            user=user,
            action=_("user deleted forum"),
            forum=forum
        )
        log.save()
        return log


class DeactivateQueryset(models.query.QuerySet):

    def delete(self, force=False):

        if force:
            super(DeactivateQueryset, self).delete()
        else:
            self.deactivate()

    def deactivate(self):
        self.update(is_deleted=True)


class DeactivateManager(models.Manager):

    def get_queryset(self):
        return DeactivateQueryset(self.model).filter(is_deleted=False)

    def get_full_queryset(self):
        return super(DeactivateManager, self).get_queryset()


class DeleteMixin(models.Model):

    is_deleted = models.BooleanField(default=False, db_index=True, verbose_name=_("Deleted"))

    objects = DeactivateManager()

    class Meta:
        abstract = True

    def delete(self, force=False):

        if force:
            super(DeleteMixin, self).delete()
        else:
            self.deactivate()

    def deactivate(self):

        self.is_deleted = True
        self.save()


class SingletonModel(models.Model):
    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class Message(SingletonModel):
    timestamp = models.DateTimeField(_("Timestamp"))
    text = models.CharField(_("Text"), max_length=200)

    def __str__(self):
        to_tz = timezone.get_default_timezone()
        return self.timestamp.astimezone(to_tz).strftime("%d/%m/%Y, %H:%M:%S")