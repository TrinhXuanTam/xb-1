from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView 
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect

from .models import ShopItem
from .models import ShopOrder
from .models import ShopOrderItem
from .models import ShopPayment

from .forms import OrderForm
from .forms import ShopItemForm

from ..core.views import LoginMixinView

import random

# TemplateView used for late redirect after success and failure messages
class DelayRedirectView(LoginMixinView, TemplateView):
	template_name = "delayedRedirect.html"
	def __init__(self, delay, target, kwargs, messages):
		self.delay = delay
		self.target = target
		self.redirectKwargs = kwargs
		self.messages = messages
		
	def get_context_data(self, **localKwargs):
		context = super(DelayRedirectView, self).get_context_data(**localKwargs)
		context['delay'] = self.delay
		context['target'] = reverse(self.target, kwargs=self.redirectKwargs)
		
		try:
			messageID = int(localKwargs.get('id', 0))
		except ValueError:
			messageID = 0
		
		context['message'] = self.messages[messageID]
		return context

		
#		
# Index View		
#		
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
		

#
# Cart Views
#
class CartItemAddView(RedirectView):
	permanent = False
	def get_redirect_url(self, *args, **kwargs):
		id = kwargs.get('pk', None)
		resultObject = ShopItem.objects.filter(pk=id).first()
		if resultObject == None:
			return reverse_lazy('eshop:cartItemAddFailure', kwargs={'id': 1})
		
		if resultObject.itemActive == False:
			return reverse_lazy('eshop:cartItemAddFailure', kwargs={'id': 2})
		
		if self.request.session.get('orderList', None) == None :		
			self.request.session['orderList'] = {id: 1}
		else:
			self.request.session['orderList'][id] = self.request.session['orderList'].get(id, 0) + 1 
		
		self.request.session.modified = True	
		return reverse_lazy("eshop:shopIndex")		
		
class CartItemAddFailureView(DelayRedirectView):
	def __init__(self):
		super(CartItemAddFailureView, self).__init__(5000, "eshop:shopIndex", None,
			["Something bad happened", "Item can not be found", "Item is no longer available"])
		
class CartItemRemoveView(RedirectView):
	permanent = False;
	def get_redirect_url(self, *args, **kwargs):
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


class CartItemDiscardView(RedirectView):
	permanent = False
	def get_redirect_url(self, *args, **kwargs):
		id = kwargs.get('pk', '')
		if id == '':
			self.request.session['orderList'] = None
			self.request.session.modified = True
		elif self.request.session.get('orderList', None) != None :
			self.request.session['orderList'].pop(id, None)
			self.request.session.modified = True
			if len(self.request.session['orderList']) == 0:
				self.request.session['orderList'] = None
			
		return reverse_lazy("eshop:shopIndex")		
	

#
# ShopItem Views
#
class ShopItemListView(LoginMixinView, LoginRequiredMixin, ListView):
	model = ShopItem
	template_name = "manageShopList.html"
	permission_required = "eshop.view_shopitem"
	
class ShopItemCreateView(LoginMixinView, LoginRequiredMixin, CreateView):
	form_class = ShopItemForm
	template_name = "manageShopAdd.html"
	success_url = reverse_lazy("eshop:manageShopList")
	permission_required = "eshop.add_shopitem"
		
class ShopItemUpdateView(LoginMixinView, LoginRequiredMixin, UpdateView):
	model = ShopItem
	form_class = ShopItemForm
	template_name = "manageShopAdd.html"
	success_url = reverse_lazy("eshop:manageShopList")
	permission_required = "eshop.change_shopitem"
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
		

#
# Order Views		
#		
class OrderListView(LoginMixinView, LoginRequiredMixin, ListView):
	model = ShopOrder
	template_name = "manageOrderList.html"
	permission_required = "eshop.view_shoporder"
	
class OrderRemoveView(LoginMixinView, LoginRequiredMixin, DeleteView):
	model = ShopOrder
	template_name = "manageOrderRemove.html"
	success_url = reverse_lazy("eshop:manageOrderList")
	permission_required = "eshop.delete_shoporder"
	
class OrderPayView(LoginMixinView, LoginRequiredMixin, RedirectView):
	permanent = False
	permission_required = "eshop.update_shoporder"
	def get_redirect_url(self, *args, **kwargs):
		try:
			id = int(kwargs.get('pk', None))
		except ValueError:
			return reverse_lazy('eshop:manageOrderPayFailure', kwargs={'id': 1})
			
		order = ShopOrder.objects.filter(pk = id).first()
		if order == None:
			return reverse('eshop:manageOrderPayFailure', kwargs={'id': 2})
		
		payment = ShopPayment.objects.filter(paymentOrder = order).first()
		if payment == None:
			return reverse('eshop:manageOrderPayFailure', kwargs={'id': 3})
		
		payment.paymentReceived = True
		payment.save()
		
		return reverse_lazy('eshop:manageOrderList')
	
class OrderPayFailureView(DelayRedirectView):
	def __init__(self):
		super(OrderPayFailureView, self).__init__(5000, "eshop:manageOrderList", None,
			["Something bad happened", "Bad address, only numbers can be use", "Order not found", "Payment not found"])
	
class OrderCreateView(LoginMixinView, FormView):
	template_name = "manageOrderCreate.html"
	form_class = OrderForm
	success_url = reverse_lazy("eshop:shopIndex")
	def render_to_response(self, context):
		if self.request.session.get('orderList', None) == None :
			return redirect(reverse('eshop:manageOrderCreateFailure', kwargs={'id': 1}))
		return super(OrderCreateView, self).render_to_response(context)
		
	def form_valid(self, form):
		if self.request.session.get('orderList', None) == None :
			return reverse_lazy('eshop:manageOrderCreateFailure', kwargs={'id': 1})

		totalPrice = 0
		confirmedItems = []
		for orderItemID in self.request.session['orderList']:
			resultObject = ShopItem.objects.filter(pk=int(orderItemID)).first()
			if resultObject == None:
				return reverse_lazy('eshop:manageOrderCreateFailure', kwargs={'id': 2})
				
			if resultObject.itemActive == False:	
				return reverse_lazy('eshop:manageOrderCreateFailure', kwargs={'id': 3})

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

class OrderCreateFailureView(DelayRedirectView):
	def __init__(self):
		super(OrderCreateFailureView, self).__init__(5000, "eshop:shopIndex", None,
			["Something bad happened", "Empty cart can not be ordered", "Item in your cart doesn't exist, reset cart", "Item in your cart is no longer available, reset cart"])		
