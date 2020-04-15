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
	#itemImg = TODO - will be implemented later
	itemDesc = models.CharField("Description", max_length = 200);
	itemType = models.PositiveSmallIntegerField("Item type", choices=TYPE_CHOICES, default=NONE)
	itemActive = models.BooleanField("Active", default=True);