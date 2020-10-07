from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

import random

class ShopItem(models.Model):
	"""
	ShopItem is object which contains all informations about each items in shop
	NOTE: Any change to object should create new object with new values
	"""
	
	TOP = 0
	SALE = 1
	NONE = 2
	NEW = 3

	TYPE_CHOICES = (
		(TOP, "Top"),
		(SALE, "Sale"),
		(NONE, "None"),
		(NEW, "New")
	)
	
	itemName = models.CharField("Název produktu", max_length = 50)
	itemPrice = models.DecimalField("Cena", decimal_places=2, max_digits=10)
	itemImg = models.ImageField(_("Image"), default='default.jpg', upload_to='ShopItems', blank=True, null=True)
	itemDesc = models.TextField(_("Detail"))
	itemType = models.PositiveSmallIntegerField("Typ produktu", choices=TYPE_CHOICES, default=NONE)
	itemActive = models.BooleanField("Aktivovat", default=True)
	
class ShopOrder(models.Model):
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
		
		slg = random.randint(100, 5000)
		while ShopOrder.objects.filter(orderSlug=slg).exists():
			orderSlug = orderSlug + "_" + str(random.randint(0, 1000))
		self.orderSlug = slg
	
class ShopPayment(models.Model):
	"""
	ShopPayment is connected to ShopOrder, each order has own instance of ShopPayment.
	This object contains all informations about state of payment, include if is payed or not
	"""
	
	paymentPrice = models.DecimalField("TotalPrice", decimal_places=2, max_digits=12)
	paymentReceived = models.BooleanField("Received", default = False)
	paymentVariableSymbol = models.DecimalField("VariableSymbol", decimal_places = 0, max_digits = 10)
	paymentSpecificSymbol = models.DecimalField("SpecificSymbol", decimal_places = 0, max_digits = 10)
	paymentOrder = models.ForeignKey(ShopOrder, verbose_name="ShopOrder", on_delete = models.CASCADE, blank = True, null = True)
	
class ShopOrderItem(models.Model):
	"""
	ShopOrderItem is used as connection between ShopItem and ShopOrder
	One ShopOder instance can have many of ShopOrderItem instances of different ShopItem liked to it.
	NOTE: By changing values in ShopItem this object remains linked to old one 
	"""
	
	shopItem = models.ForeignKey(ShopItem, verbose_name="ShopItem", on_delete = models.PROTECT, blank=True, null=True)
	shopOrder = models.ForeignKey(ShopOrder, verbose_name="ShopOrder", on_delete = models.CASCADE, blank=True, null=True)
	shopItemCount = models.DecimalField("ItemCount", decimal_places=0, max_digits=10)
	