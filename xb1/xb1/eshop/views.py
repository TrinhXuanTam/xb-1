import datetime

from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
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
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import transaction


from .models import ShopItem
from .models import ShopOrder
from .models import ShopOrderItem
from .models import ShopPayment

from .forms import OrderForm
from .forms import ShopItemForm

from ..core.views import LoginMixinView
from ..settings import EMAIL_HOST_USER
from ..settings import ESHOP_BANK_ACCOUNT

import random

class DelayRedirectView(LoginMixinView, TemplateView):
	"""
	Custom RedicetView
	Used for display error message or confirmation and forcing redirect by JS to target page
	"""

	template_name = "delayedRedirect.html"

	def __init__(self, delay, target, kwargs, messages):
		self.delay = delay
		self.target = target
		self.redirectKwargs = kwargs
		self.messages = messages

	def get_context_data(self, **localKwargs):
		"""
		Set values to context and get message if is any present
		"""
		context = super(DelayRedirectView, self).get_context_data(**localKwargs)
		context['delay'] = self.delay
		context['target'] = reverse(self.target, kwargs=self.redirectKwargs)

		# Find and set message text if id is set
		try:
			messageID = int(localKwargs.get('id', 0))
		except ValueError:
			messageID = 0

		context['message'] = self.messages[messageID]
		return context


class ShopIndex(LoginMixinView, ListView):
	"""
	ShopIndex is used for manipulate with context of Index page, adding items in bucket and items in shop
	page: ^$
	"""

	model = ShopItem
	template_name = "eshop.html"

	def get_context_data(self, **kwargs):
		context = super(ShopIndex, self).get_context_data(**kwargs)
		# Check if any item is in the shop list
		if self.request.session.get('orderList', None) == None:
			context['totalPrice'] = 0;
			context['totalCount'] = 0;
			return context

		# Calculate total price and rearrange store items in that list for being displayeds
		totalPrice = 0;
		context['orderItems'] = [];
		for shopItem in self.object_list:
			for orderItem in self.request.session['orderList']:
				if shopItem.pk == int(orderItem):
					context['orderItems'].append((shopItem, self.request.session['orderList'][orderItem]));
					totalPrice += self.request.session['orderList'][orderItem] * shopItem.itemPrice;

		context['totalPrice'] = totalPrice;
		context['totalCount'] = len(context['orderItems']);

		return context


class CartItemAddView(RedirectView):
	"""
	Used for adding item to shop list and redirecting back.
	page: ^manage/cart/add/(?P<pk>[0-9]+)$
	note: If item is already present, count is incresed
	"""

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
		messages.success(self.request, 'Cart was updated.')
		return reverse_lazy("eshop:shopIndex")


class CartItemAddFailureView(DelayRedirectView):
	"""
	In case of failure adding new item into shop list, see cause list in note
	page: ^manage/cart/add/failure/(?P<id>[0-9]+)$
	note: Item does not exist. Item is not active.
	"""

	def __init__(self):
		super(CartItemAddFailureView, self).__init__(5000, "eshop:shopIndex", None,
			[_("Something bad happened"), _("Item can not be found"), _("Item is no longer available")])

class CartItemRemoveView(RedirectView):
	"""
	Used for removing item by one from shop list and redirecting back.
	page: ^manage/cart/remove/(?P<pk>[0-9]+)$
	note: If list become empty, will be destroyed. If count of order is 0 or less item is fully removed from order.
	"""

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
			messages.success(self.request, 'Cart was updated.')

		return reverse_lazy("eshop:shopIndex")


class CartItemDiscardView(RedirectView):
	"""
	Used for removing all items or one item fully from shop list and redirecting back.
	page: ^manage/cart/discard/$ , ^manage/cart/discard/(?P<pk>[0-9]+)$
	note: Clear all or just one item.
	"""

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
		messages.success(self.request, 'Cart was updated.')
		return reverse_lazy("eshop:shopIndex")

class ShopItemListView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
	"""
	Display all ShopItems in list also with values of each instance
	page: ^manage/shop/list/$
	admin: yes
	"""

	model = ShopItem
	template_name = "manageShopList.html"
	permission_required = "eshop.view_shopitem"

class ShopItemCreateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	"""
	Create new ShopItem
	page: ^manage/shop/add/$
	admin: yes
	"""

	form_class = ShopItemForm
	template_name = "manageShopAdd.html"
	success_url = reverse_lazy("eshop:manageShopList")
	permission_required = "eshop.add_shopitem"

class ShopItemUpdateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	"""
	Create new ShopItem from old one by updating old values with new one.
	page: ^manage/shop/update/(?P<pk>[0-9]+)$
	admin: yes
	"""
	model = ShopItem
	form_class = ShopItemForm
	template_name = "manageShopEdit.html"
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
class OrderListView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, ListView):
	"""
	Display all ShopOrder in list also with values of each instance
	page: ^manage/order/list/$
	admin: yes
	"""

	model = ShopOrder
	template_name = "manageOrderList.html"
	permission_required = "eshop.view_shoporder"


class OrderRemoveView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	"""
	Remove ShopOrder from system, Cascade remove is used. Payment will be removed as well
	page: ^manage/order/remove/(?P<pk>[0-9]+)$
	admin: yes
	"""

	model = ShopOrder
	template_name = "manageOrderRemove.html"
	success_url = reverse_lazy("eshop:manageOrderList")
	permission_required = "eshop.delete_shoporder"


class OrderPayView(LoginMixinView, LoginRequiredMixin, RedirectView):
	"""
	Set payment status of ShopOder to True
	page: ^manage/order/remove/(?P<pk>[0-9]+)$
	admin: yes
	"""

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
	"""
	In case of failure confirmation of payment
	page: ^manage/order/pay/failure/(?P<id>[0-9]+)$
	note: Order does not exist.
	admin: yes
	"""
	def __init__(self):
		super(OrderPayFailureView, self).__init__(5000, "eshop:manageOrderList", None,
			[_("Something bad happened"), _("Bad address, only numbers can be use"), _("Order not found"), _("Payment not found")])


class OrderCreateView(LoginMixinView, FormView):
	"""
	Create new order from all items in order list
	page: ^manage/order/create/$
	admin: no
	note: List is cleared after order
	"""

	template_name = "manageOrderCreate.html"
	form_class = OrderForm
	success_url = reverse_lazy("eshop:shopIndex")

	def render_to_response(self, context):
		if self.request.session.get('orderList', None) == None :
			return redirect(reverse('eshop:manageOrderCreateFailure', kwargs={'id': 1}))

		# Use information from profile
		if not self.request.user.is_anonymous:
			user = self.request.user
			context['form'].fields['orderFirstName'].initial = user.profile.name
			context['form'].fields['orderLastName'].initial = user.profile.surname
			context['form'].fields['orderEmail'].initial = user.email
			context['form'].fields['orderAddressCity'].initial = user.profile.city
			context['form'].fields['orderAddressStreet'].initial = user.profile.address
			context['form'].fields['orderAddressPostNumber'].initial = user.profile.postalCode
			context['form'].fields['orderPhone'].initial = user.profile.phone

		return super(OrderCreateView, self).render_to_response(context)

	def get_order_items(self, order):

		items_q = order.shoporderitem_set.all()
		items = []

		for i in items_q:
			items.append({
				"count": i.shopItemCount,
				"name": i.shopItem.itemName,
				"price": i.shopItem.itemPrice
			})

		return items


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
		
		try:
			with transaction.atomic():
			
				form.instance.save()
				# Create links with items
				for confirmedItem in confirmedItems:
					item = ShopOrderItem()
					item.shopItem = confirmedItem[0]
					item.shopOrder = form.instance
					item.shopItemCount = confirmedItem[1]
					item.save()

				# Create payment for this order
				payment = ShopPayment()
				payment.paymentOrder = form.instance
				payment.paymentReceived = False
				payment.paymentPrice = totalPrice	
					
				# Specific way to create variable symbol
				yearVariableSymbol = ( datetime.datetime.now().year * 1000000 ) % 10000000000
				orderVariableSymbol = ( form.instance.pk * 15 - ( random.randint(0, 29) - 15 )) % 1000000
				
				paymentVariableSymbol = yearVariableSymbol + orderVariableSymbol
				payment.paymentVariableSymbol = paymentVariableSymbol
				payment.paymentSpecificSymbol = 0	
				payment.save()
				
				subject = _("Order successfully received")
				message = render_to_string('manageOrderEmail.html', {
					'domain': get_current_site(self.request).domain,
					'slug': form.instance.orderSlug,
					'price': payment.paymentPrice,
					'vs': payment.paymentVariableSymbol,
					'ss': payment.paymentSpecificSymbol,
					'account': ESHOP_BANK_ACCOUNT,
					"items": self.get_order_items(form.instance)
				})
		
		
				send_mail(subject, message, EMAIL_HOST_USER, [str(form.instance.orderEmail)], fail_silently=False)
		except:	
			messages.warning(self.request, _("Order can not be created now, please try again later"))
			return redirect(reverse('eshop:shopIndex'))
			
		self.request.session['orderList'] = None
		messages.success(self.request, _("Order was created. Mail with payment info was sent to your email address."))
		
		return super(OrderCreateView, self).form_valid(form)

class OrderCreateFailureView(DelayRedirectView):
	"""
	In case of failure creating an order, see note for cause.
	page: ^manage/order/create/failure/(?P<id>[0-9]+)$
	note: Empty cart, Bad item in cart
	admin: no
	"""

	def __init__(self):
		super(OrderCreateFailureView, self).__init__(5000, "eshop:shopIndex", None,
			[_("Something bad happened"), _("Empty cart can not be ordered"),
			_("Item in your cart doesn't exist, reset cart"),
			_("Item in your cart is no longer available, reset cart")
		])


class OrderTrackerView(LoginMixinView, TemplateView):
	"""
	Used for display information about order, used by link from email
	page: ^manage/order/tracker/(?P<slug>[\w-]+)/$
	admin: no
	"""

	template_name = "manageOrderTracker.html"

	def dispatch(self, request, *args, **kwargs):
		result = ShopOrder.objects.filter(orderSlug = kwargs['slug']).first()
		if result is None:
			return redirect(reverse('eshop:manageOrderFailureTracker', kwargs={'id': 1}))
		return super(OrderTrackerView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(OrderTrackerView, self).get_context_data(**kwargs)
		context['order'] = ShopOrder.objects.filter(orderSlug = kwargs['slug']).first()
		context['admin'] = self.request.user and self.request.user.has_perm('core.view_user')
		context['orderItems'] = ShopOrderItem.objects.filter(shopOrder = context['order']) 

		return context


class OrderTrackerFailureView(DelayRedirectView):
	"""
	In case of failure tracking order, see note for cause.
	page: ^manage/order/tracker/failure/(?P<id>[0-9]+)$
	note: Malformed id of order
	admin: no
	"""

	def __init__(self):
		super(OrderTrackerFailureView, self).__init__(5000, "eshop:shopIndex", None,
			[_("Something bad happened"), _("Order related with this tracker doesn't exists")])
