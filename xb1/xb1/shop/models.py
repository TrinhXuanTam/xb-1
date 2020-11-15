from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..core.models import DeleteMixin
from ..core.models import User

from django.utils import timezone

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

class Price(DeleteMixin):

    price = models.FloatField(_("Product price"))
    since = models.DateTimeField(_("Since"))
    till = models.DateTimeField(_("Till"))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True)

class Specification(DeleteMixin):

    name = models.CharField(_("Specification"), max_length = 50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True)

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

class CartEntry(DeleteMixin):

    count = models.IntegerField(_("Count"))
    price = models.ForeignKey(Price, on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True)
    specification = models.ManyToManyField(SpecificationEntry, blank=True)
    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete = models.CASCADE, blank=True, null=True)

    @property
    def total(self):
        return self.count * self.price.price

class Cart():
    
    def __init__(self, memory=[]):
        self.memory = memory

    def add(self, item, count):
        for entryID in self.memory:
            entry = CartEntry.objects.filter(pk=entryID).first()
            if entry.item.pk == item.pk:
                entry.count += count
                entry.save()
                return None

        entry = CartEntry()
        entry.count = count
        entry.price = item.price
        entry.item = item
        entry.order = None
        entry.save()

        self.memory.append(entry.pk)
        return None

    def set(self, item, count):
        pass

    def get(self, item):
        pass

    def asTemplate(self):
        result = []
        for entryID in self.memory:
            entry = CartEntry.objects.filter(pk=entryID).first()
            result.append(entry)
        
        return result