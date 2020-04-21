from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.views.generic import View
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import ShopItem
from .models import ShopOrderItem

from .forms import OrderForm
from .forms import ShopItemForm

from ..core.views import LoginMixinView

class ShopItemCreateView(LoginMixinView, LoginRequiredMixin, View):
	form_class = ShopItemForm
	template_name = "eshopAddItem.html"
	success_url = reverse_lazy("eshop:shopItemCreate")
		
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
	template_name = "eshopOrder.html"
	form_class = OrderForm
	success_url = reverse_lazy("eshop:shopIndex")
	def render_to_response(self, context):
		if self.request.session.get('orderList', None) == None :
			return redirect('eshop:shopIndex')
		return super(OrderCreateView, self).render_to_response(context)
		
	def form_valid(self, form):
		if self.request.session.get('orderList', None) == None :
			return redirect('eshop:shopIndex')

		confirmedItems = []
		for orderItemID in self.request.session['orderList']:
			resultObject = ShopItem.objects.filter(pk=int(orderItemID)).first()
			if resultObject == None:
				return redirect('eshop:shopIndex')
				
			if resultObject.itemActive == False:	
				return redirect('eshop:shopIndex')

			confirmedItems.append((resultObject, self.request.session['orderList'][orderItemID]))
			
		form.instance.save()

		for confirmedItem in confirmedItems:
			item = ShopOrderItem()
			item.shopItem = confirmedItem[0]
			item.shopOrder = form.instance
			item.shopItemCount = confirmedItem[1]
			item.save()

		self.request.session['orderList'] = None
	
		return super(OrderCreateView, self).form_valid(form)
	
class OrderItemRemoveAllView(RedirectView):
	permanent = False
	def get_redirect_url(self, *args, **kwargs):
		requestID = self.request.GET.get('id', '')
		if requestID == '':
			self.request.session['orderList'] = None
			self.request.session.modified = True
			return reverse_lazy("eshop:shopIndex")
		
		if self.request.session.get('orderList', None) != None :
			self.request.session['orderList'].pop(requestID, None)
			self.request.session.modified = True
			if len(self.request.session['orderList']) == 0:
				self.request.session['orderList'] = None
			
			
		return reverse_lazy("eshop:shopIndex")
	
class OrderItemRemoveView(RedirectView):
	permanent = False;
	def get_redirect_url(self, *args, **kwargs):
		requestID = self.request.GET.get('id', '')
		if requestID == '':
			return reverse_lazy("eshop:shopIndex")
		
		if self.request.session.get('orderList', None) != None:
			if self.request.session['orderList'].get(requestID, 0) - 1 < 1:
				self.request.session['orderList'].pop(requestID, None)
				if len(self.request.session['orderList']) == 0:
					self.request.session['orderList'] = None
			else:
				self.request.session['orderList'][requestID] = self.request.session['orderList'].get(requestID, 0) - 1 
				
			self.request.session.modified = True
			
		return reverse_lazy("eshop:shopIndex")	
	
class OrderItemAddView(RedirectView):
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
		
		if self.request.session.get('orderList', None) == None :		
			self.request.session['orderList'] = {requestID: 1}
		else:
			self.request.session['orderList'][requestID] = self.request.session['orderList'].get(requestID, 0) + 1 
		
		self.request.session.modified = True	
		return reverse_lazy("eshop:shopIndex")