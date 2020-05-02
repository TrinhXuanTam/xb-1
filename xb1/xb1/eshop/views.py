from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView 
from django.views.generic.base import RedirectView
from django.views.generic import View
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import ShopItem
from .models import ShopOrder
from .models import ShopOrderItem
from .models import ShopPayment

from .forms import OrderForm
from .forms import ShopItemForm

from ..core.views import LoginMixinView

import random

class ShopItemCreateView(LoginMixinView, LoginRequiredMixin, CreateView):
	form_class = ShopItemForm
	template_name = "manageShopAdd.html"
	success_url = reverse_lazy("eshop:manageShopList")
		
class ShopItemListView(LoginMixinView, LoginRequiredMixin, ListView):
	model = ShopItem
	template_name = "manageShopList.html"
	
class ShopItemUpdateView(LoginMixinView, LoginRequiredMixin, UpdateView):
	model = ShopItem
	form_class = ShopItemForm
	template_name = "manageShopAdd.html"
	success_url = reverse_lazy("eshop:manageShopList")
	def form_valid(self, form):
		resultObject = ShopOrderItem.objects.filter(shopItem=form.instance).first()
		if resultObject == None:
			return super(ShopItemUpdateView, self).form_valid(form)
			
		resultObject = ShopItem.objects.filter(pk=form.instance.pk).first()
		resultObject.itemActive = False
		resultObject.save()
		
		form.instance.pk = None
		form.instance.save()
		
		return redirect('eshop:manageShopList')
		
class OrderListView(LoginMixinView, LoginRequiredMixin, ListView):
	model = ShopOrder
	template_name = "manageOrderList.html"
	
class OrderRemoveView(LoginMixinView, LoginRequiredMixin, DeleteView):
	model = ShopOrder
	template_name = "manageOrderRemove.html"
	success_url = reverse_lazy("eshop:manageOrderList")
	
class OrderPayView(LoginMixinView, LoginRequiredMixin, RedirectView):
	permanent = False
	def get_redirect_url(self, *args, **kwargs):
		if kwargs.get('pk', None) == None:
			return reverse_lazy('eshop:manageOrderList')
		
		id = -1
		try:
			id = int(kwargs.get('pk', None))
		except ValueError:
			return reverse_lazy('eshop:manageOrderList')
			
		order = ShopOrder.objects.filter(pk = id).first()
		if order == None:
			return reverse_lazy('eshop:manageOrderList')
		
		payment = ShopPayment.objects.filter(paymentOrder = order).first()
		if payment == None:
			return reverse_lazy('eshop:manageOrderList')
		
		payment.paymentReceived = True
		payment.save()
		
		return reverse_lazy('eshop:manageOrderList')
		
class ShopIndex(LoginMixinView, ListView):
	model = ShopItem
	template_name = "eshop.html"
	def get_context_data(self, **kwargs):
		context = super(ShopIndex, self).get_context_data(**kwargs)
		if self.request.session.get('orderList', None) == None:
			context['totalPrice'] = 0;
			return context
		
		totalPrice = 0;
		context['orderItems'] = [];	
		for shopItem in self.object_list:
			for orderItem in self.request.session['orderList']:
				if shopItem.pk == int(orderItem):
					context['orderItems'].append((shopItem, self.request.session['orderList'][orderItem]));
					totalPrice += self.request.session['orderList'][orderItem] * shopItem.itemPrice;
					
		context['totalPrice'] = totalPrice;
		
		return context

class OrderCreateView(LoginMixinView, FormView):
	template_name = "manageOrderCreate.html"
	form_class = OrderForm
	success_url = reverse_lazy("eshop:shopIndex")
	def render_to_response(self, context):
		if self.request.session.get('orderList', None) == None :
			return redirect('eshop:shopIndex')
		return super(OrderCreateView, self).render_to_response(context)
		
	def form_valid(self, form):
		if self.request.session.get('orderList', None) == None :
			return redirect('eshop:shopIndex')

		totalPrice = 0
		confirmedItems = []
		for orderItemID in self.request.session['orderList']:
			resultObject = ShopItem.objects.filter(pk=int(orderItemID)).first()
			if resultObject == None:
				return redirect('eshop:shopIndex')
				
			if resultObject.itemActive == False:	
				return redirect('eshop:shopIndex')

			totalPrice += self.request.session['orderList'][orderItemID] * resultObject.itemPrice;
			confirmedItems.append((resultObject, self.request.session['orderList'][orderItemID]))
			
		form.instance.save()

		for confirmedItem in confirmedItems:
			item = ShopOrderItem()
			item.shopItem = confirmedItem[0]
			item.shopOrder = form.instance
			item.shopItemCount = confirmedItem[1]
			item.save()

		payment = ShopPayment()	
		payment.paymentOrder = form.instance
		payment.paymentReceived = False
		payment.paymentPrice = totalPrice
		payment.paymentVariableSymbol = form.instance.pk % 9999999999
		payment.paymentSpecificSymbol = random.randint(0, 9999999999)
		payment.save()
		
		self.request.session['orderList'] = None
	
		return super(OrderCreateView, self).form_valid(form)
	
class CartItemDiscardView(RedirectView):
	permanent = False
	def get_redirect_url(self, *args, **kwargs):
		id = kwargs.get('pk', '')
		if id == '':
			self.request.session['orderList'] = None
			self.request.session.modified = True
			return reverse_lazy("eshop:shopIndex")
		
		if self.request.session.get('orderList', None) != None :
			self.request.session['orderList'].pop(id, None)
			self.request.session.modified = True
			if len(self.request.session['orderList']) == 0:
				self.request.session['orderList'] = None
			
		return reverse_lazy("eshop:shopIndex")
	
class CartItemRemoveView(RedirectView):
	permanent = False;
	def get_redirect_url(self, *args, **kwargs):
		if kwargs.get('pk', None) == None:
			return reverse_lazy('eshop:manageOrderList')
		id = kwargs.get('pk', None)

		if self.request.session.get('orderList', None) != None:
			if self.request.session['orderList'].get(id, 0) - 1 < 1:
				self.request.session['orderList'].pop(id, None)
				if len(self.request.session['orderList']) == 0:
					self.request.session['orderList'] = None
			else:
				self.request.session['orderList'][id] = self.request.session['orderList'].get(id, 0) - 1 
				
			self.request.session.modified = True
			
		return reverse_lazy("eshop:shopIndex")	
	
class CartItemAddView(RedirectView):
	permanent = False
	def get_redirect_url(self, *args, **kwargs):
		if kwargs.get('pk', None) == None:
			return reverse_lazy('eshop:manageOrderList')
		id = kwargs.get('pk', None)

		resultObject = ShopItem.objects.filter(pk=id).first()
		if resultObject == None:
			return reverse_lazy("eshop:shopIndex")
		
		if resultObject.itemActive == False:
			return reverse_lazy("eshop:shopIndex")
		
		print("X")
		
		if self.request.session.get('orderList', None) == None :		
			self.request.session['orderList'] = {id: 1}
		else:
			self.request.session['orderList'][id] = self.request.session['orderList'].get(id, 0) + 1 
		
		self.request.session.modified = True	
		return reverse_lazy("eshop:shopIndex")