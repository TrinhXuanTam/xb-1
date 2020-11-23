from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import serializers

from ..core.models import DeleteMixin
from ..core.models import User

from django.utils import timezone

import random

class Item(DeleteMixin):

    name = models.CharField(_("Product name"), max_length = 50)
    image = models.ImageField(_("Product image"), default='default.jpg', upload_to='ShopItems', blank=True, null=True)
    desc = models.CharField(_("Product description"), max_length=400)

    @property
    def price(self):
        prices = Price.objects.filter(item=self)
        for price in prices:
            if price.till >= timezone.now():
                return price
        return None

    @property
    def specification(self):
        return Specification.objects.filter(item=self, active=True).first()    

class Price(DeleteMixin):

    price = models.FloatField(_("Product price"))
    since = models.DateTimeField(_("Since"))
    till = models.DateTimeField(_("Till"))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True)

class Specification(DeleteMixin):

    name = models.CharField(_("Specification"), max_length = 50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True)
    active = models.BooleanField(_("Active"), blank=True)

    @property
    def entry(self):
        return SpecificationEntry.objects.filter(specification=self).all() 

class SpecificationEntry(DeleteMixin):

    value = models.CharField(_("Value"), max_length = 50)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, blank=True)

class Order(DeleteMixin):

    firstname = models.CharField(_("Name"), max_length=100, null=True, blank=True)
    lastname = models.CharField(_("Surname"), max_length=100, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length = 64)
    city = models.CharField(_("City"), max_length=100, null=True, blank=True)
    street = models.CharField(_("Address"), max_length=100, null=True, blank=True)
    post = models.CharField(_("Postal Code"), max_length=10, null=True, blank=True)
    phone = models.CharField(_("Phone"), max_length=20, null=True, blank=True)
    slug = models.SlugField(verbose_name=_("Slug"), unique=True, max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete = models.PROTECT, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.generate_slug()
        
        super().save(*args, **kwargs)

    def generate_slug(self):
        slug = random.randint(100000000, 9999999999)
        while Order.objects.filter(slug=slug).exists():
            slug = random.randint(100000000, 9999999999)
        self.slug = slug

    @property
    def cart(self):
        return Cart.objects.filter(order=self).first()

    @property
    def payment(self):
        return Payment.objects.filter(order=self).first()

class Cart(DeleteMixin):

    creation = models.DateTimeField(verbose_name=_('Creation date'))
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete = models.CASCADE, blank=True, null=True)

    @property
    def entries(self):
        return CartEntry.objects.filter(cart=self).all()

    @property
    def total(self):
        total = 0
        for entry in CartEntry.objects.filter(cart=self).all():
            total += entry.total
        return total

class CartEntry(DeleteMixin):

    count = models.IntegerField(_("Count"))
    price = models.ForeignKey(Price, on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True)
    specification = models.ForeignKey(SpecificationEntry, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart, verbose_name=_("Cart"), on_delete = models.CASCADE, blank=True, null=True)

    @property
    def total(self):
        return self.count * self.price.price

class Payment(DeleteMixin):

	received = models.BooleanField(_("Received"), default = False)
	variableSymbol = models.DecimalField(_("VariableSymbol"), decimal_places = 0, max_digits = 10)
	specificSymbol = models.DecimalField(_("SpecificSymbol"), decimal_places = 0, max_digits = 10)
	order = models.ForeignKey(Order, verbose_name=_("ShopOrder"), on_delete = models.CASCADE, blank = True, null = True)
