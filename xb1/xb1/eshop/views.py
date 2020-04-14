from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
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
	
# class 