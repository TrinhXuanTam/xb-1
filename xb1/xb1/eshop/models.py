from django.db import models

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
	
	itemName = models.CharField("Name", max_length = 20)
	itemPrice = models.DecimalField("Price", decimal_places=2, max_digits=10)
	itemImg = models.ImageField("Image", default='default.jpg', upload_to='ShopItems')
	itemDesc = models.CharField("Description", max_length = 200);
	itemType = models.PositiveSmallIntegerField("Item type", choices=TYPE_CHOICES, default=NONE)
	itemActive = models.BooleanField("Active", default=True);
	
class ShopOrder(models.Model):
	orderFirstName = models.CharField("FirstName", max_length = 30)
	orderLastName = models.CharField("LastName", max_length = 30)
	orderEmail = models.EmailField("Email", max_length = 64)
	orderAddressCity = models.CharField("City", max_length = 20)
	orderAddressStreet = models.CharField("Street", max_length = 20)
	orderAddressStreetNumber = models.DecimalField("StreetNumber", decimal_places=0, max_digits=5)
	orderAddressPostNumber = models.DecimalField("PostNumber", decimal_places=0, max_digits=5)

	@property
	def isPaid(self):
		resultObject = ShopPayment.objects.filter(paymentOrder=self).first()
		if resultObject == None:
			return False
		return resultObject.paymentReceived
	
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
	