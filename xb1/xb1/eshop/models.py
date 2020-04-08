from django.db import models

# Create your models here.

class ShopItem(models.Model):
	
	itemName = models.CharField("Name", max_length = 20)
	itemPrice = models.CharField("Price", max_length = 10)
	#itemImg -> Odkaz nebo Pure data ?
	itemDesc = models.CharField("Description", max_length = 200);
	#itemType -> TOP/SALE/NONE/NEW -> radioButton
	itemActive = models.BooleanField("Active", default=True);