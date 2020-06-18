from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

import random

class ShopItem(models.Model):

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
	
	itemName = models.CharField("Název produktu", max_length = 20)
	itemPrice = models.DecimalField("Cena", decimal_places=2, max_digits=10)
	itemImg = models.ImageField(_("Image"), default='default.jpg', upload_to='ShopItems', blank=True, null=True)
	itemDesc = models.CharField(_("Detail"), max_length = 200)
	itemType = models.PositiveSmallIntegerField("Typ produktu", choices=TYPE_CHOICES, default=NONE)
	itemActive = models.BooleanField("Aktivovat", default=True)
	
class ShopOrder(models.Model):
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
		slg = random.randint(100, 5000)
		while ShopOrder.objects.filter(orderSlug=slg).exists():
			orderSlug = orderSlug + "_" + str(random.randint(0, 1000))
		self.orderSlug = slg
	
class ShopPayment(models.Model):
	paymentPrice = models.DecimalField("TotalPrice", decimal_places=2, max_digits=12)
	paymentReceived = models.BooleanField("Received", default = False)
	paymentVariableSymbol = models.DecimalField("VariableSymbol", decimal_places = 0, max_digits = 10)
	paymentSpecificSymbol = models.DecimalField("SpecificSymbol", decimal_places = 0, max_digits = 10)
	paymentOrder = models.ForeignKey(ShopOrder, verbose_name="ShopOrder", on_delete = models.CASCADE, blank = True, null = True)
	
class ShopOrderItem(models.Model):
	shopItem = models.ForeignKey(ShopItem, verbose_name="ShopItem", on_delete = models.PROTECT, blank=True, null=True)
	shopOrder = models.ForeignKey(ShopOrder, verbose_name="ShopOrder", on_delete = models.CASCADE, blank=True, null=True)
	shopItemCount = models.DecimalField("ItemCount", decimal_places=0, max_digits=10)
	