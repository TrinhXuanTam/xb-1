from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from ..core.models import DeleteMixin
from ..core.models import User

import random


class ShopItem(DeleteMixin):
	"""
	ShopItem is object which contains all informations about each items in shop
	NOTE: Any change to object should create new object with new values
	"""

	TOP = 0
	SALE = 1
	NONE = 2
	NEW = 3
	DISCOUNT = 4

	TYPE_CHOICES = (
		(TOP, _("Top")),
		(SALE, _("Sale")),
		(NONE, _("None")),
		(NEW, _("New")),
		(DISCOUNT, _("Discount")),
	)

	itemName = models.CharField(_("Product name"), max_length = 50)
	itemPrice = models.DecimalField(_("Price"), decimal_places=2, max_digits=10)
	itemImg = models.ImageField(_("Image"), default='default.jpg', upload_to='ShopItems', blank=True, null=True)
	itemDesc = models.CharField(_("Detail"), max_length=400)
	itemType = models.PositiveSmallIntegerField(_("Product type"), choices=TYPE_CHOICES, default=NONE)
	itemActive = models.BooleanField(_("Activate"), default=True)

	def __str__(self):
		return self.itemName


class ShopOrder(DeleteMixin):
	"""
	ShopOrder is used for storing all information about order, each order has own instance of object
	NOTE: This object does not contain information about ordered items
	"""

	orderFirstName =  models.CharField(_("Name"), max_length=100, null=True, blank=True)
	orderLastName = models.CharField(_("Surname"), max_length=100, null=True, blank=True)
	orderEmail = models.EmailField(_("Email"), max_length = 64)
	orderAddressCity = models.CharField(_("City"), max_length=100, null=True, blank=True)
	orderAddressStreet = models.CharField(_("Address"), max_length=100, null=True, blank=True)
	orderAddressPostNumber = models.CharField(_("Postal Code"), max_length=10, null=True, blank=True)
	orderPhone = models.CharField(_("Phone"), max_length=20, null=True, blank=True)
	orderSlug = models.SlugField(verbose_name=_("Slug"), unique=True, max_length=100, blank=True, null=True)
	orderUser = models.ForeignKey(User, verbose_name=_("User"), on_delete = models.PROTECT, blank=True, null=True)

	@property
	def isPaid(self):
		resultObject = ShopPayment.objects.filter(paymentOrder=self).first()
		if resultObject == None:
			return False
		return resultObject.paymentReceived

	def save(self, *args, **kwargs):
		if self.orderSlug is None:
			self.generate_slug()
		super().save(*args, **kwargs)

	def generate_slug(self):
		"""
		Specific method to generate slug, used for order tracking
		"""

		slg = random.randint(100000000, 9999999999)
		while ShopOrder.objects.filter(orderSlug=slg).exists():
			orderSlug = random.randint(100000000, 9999999999)
		self.orderSlug = slg


class ShopPayment(DeleteMixin):
	"""
	ShopPayment is connected to ShopOrder, each order has own instance of ShopPayment.
	This object contains all informations about state of payment, include if is payed or not
	"""

	paymentPrice = models.DecimalField(_("TotalPrice"), decimal_places=2, max_digits=12)
	paymentReceived = models.BooleanField(_("Received"), default = False)
	paymentVariableSymbol = models.DecimalField(_("VariableSymbol"), decimal_places = 0, max_digits = 10)
	paymentSpecificSymbol = models.DecimalField(_("SpecificSymbol"), decimal_places = 0, max_digits = 10)
	paymentOrder = models.ForeignKey(ShopOrder, verbose_name=_("ShopOrder"), on_delete = models.CASCADE, blank = True, null = True)


class ShopOrderItem(DeleteMixin):
	"""
	ShopOrderItem is used as connection between ShopItem and ShopOrder
	One ShopOder instance can have many of ShopOrderItem instances of different ShopItem liked to it.
	NOTE: By changing values in ShopItem this object remains linked to old one
	"""

	shopItem = models.ForeignKey(ShopItem, verbose_name=_("ShopItem"), on_delete = models.PROTECT, blank=True, null=True)
	shopOrder = models.ForeignKey(ShopOrder, verbose_name=_("ShopOrder"), on_delete = models.CASCADE, blank=True, null=True)
	shopItemCount = models.DecimalField(_("ItemCount"), decimal_places=0, max_digits=10)
