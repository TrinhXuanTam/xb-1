from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from django.views.generic import ListView
from django.urls import reverse_lazy

from .models import ShopItem

from ..core.views import LoginMixinView

class ShopItemCreateView(LoginMixinView, LoginRequiredMixin, CreateView):
	model = ShopItem
	template_name = "eshopAddItem.html"
	success_url = reverse_lazy("eshop:shopItemCreate")
	fields = ["itemName", "itemPrice", "itemDesc", "itemType", "itemActive"]
	
class ShopIndex(LoginMixinView, ListView):
	model = ShopItem
	template_name = "eshop.html"
	
class ShopItemRemoveAllView(RedirectView):
	permanent = False
	def get_redirect_url(self, *args, **kwargs):
		print("REMOVE")
		self.request.session['orderList'] = None;
		return reverse_lazy("eshop:shopIndex")
	
class ShopItemAddView(RedirectView):
	permanent = False
	def get_redirect_url(self, *args, **kwargs):
		requestID = self.request.GET.get('id', '')
		if requestID == '':
			return reverse_lazy("eshop:shopIndex")
		
		resultObject = ShopItem.objects.filter(pk=requestID).first()
		if resultObject == None:
			return reverse_lazy("eshop:shopIndex")
		
		if resultObject.itemActive == False:
			return reverse_lazy("eshop:shopIndex")
		print("SET")				
		self.request.session['orderList'] = "TEST"
			
		return reverse_lazy("eshop:shopIndex")