from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect
from django.core import serializers
from django.utils import timezone
from django.db import transaction
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives

from ..core.views import LoginMixinView
from .models import Item, Price, CartEntry, Specification, SpecificationEntry, Order, Payment
from .cart import Cart
from .forms import ItemCreateForm, ItemUpdateForm, OrderCreateForm
from ..settings import EMAIL_HOST_USER, ESHOP_BANK_ACCOUNT

import datetime
import random

class ShopIndex(LoginMixinView, ListView):

    model = Item
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        context = super(ShopIndex, self).get_context_data(**kwargs)
        context["cart"] = Cart(self.request)

        return context

class CartInsertItemView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if kwargs.get('pk', None) is None:
            messages.warning(self.request, _("Unknown key"))
            return reverse_lazy("shop:shopView")

        item = Item.objects.filter(pk = kwargs.get('pk')).first()
        if not item:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy("shop:shopView")

        cart = Cart(self.request)
        cart.insert(item)

        messages.success(self.request, _('Cart was updated.'))
        return reverse_lazy("shop:shopView")

class CartAddItemView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if kwargs.get('pk', None) is None:
            messages.warning(self.request, _("Unknown key"))
            return reverse_lazy("shop:shopView")

        entry = CartEntry.objects.filter(pk = kwargs.get('pk')).first()
        if not entry:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy("shop:shopView")

        cart = Cart(self.request)
        cart.add(entry.pk, 1)

        messages.success(self.request, _('Cart was updated.'))
        return reverse_lazy("shop:shopView")

class CartRemoveItemView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if kwargs.get('pk', None) is None:
            messages.warning(self.request, _("Unknown key"))
            return reverse_lazy("shop:shopView")

        entry = CartEntry.objects.filter(pk = kwargs.get('pk')).first()
        if not entry:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy("shop:shopView")

        cart = Cart(self.request)
        cart.remove(entry.pk, 1)

        messages.success(self.request, _('Cart was updated.'))
        return reverse_lazy("shop:shopView")

class CartDiscardItemView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if kwargs.get('pk', None) is None:
            cart = Cart(self.request)
            cart.discard(None)

        else:
            entry = CartEntry.objects.filter(pk = kwargs.get('pk')).first()
            if not entry:
                messages.warning(self.request, _("Not found"))
                return reverse_lazy("shop:shopView")

            cart = Cart(self.request)
            cart.discard(entry.pk)

        messages.success(self.request, _('Cart was updated.'))
        return reverse_lazy("shop:shopView")

class CartSetSpecificationView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if kwargs.get('pk', None) is None or kwargs.get('spec', None) is None:
            messages.warning(self.request, _("Unknown key"))
            return reverse_lazy("shop:shopView")

        entry = CartEntry.objects.filter(pk = kwargs.get('pk')).first()
        if not entry:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy("shop:shopView")

        specentry = SpecificationEntry.objects.filter(pk = kwargs.get('spec')).first()  
        if not specentry:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy("shop:shopView")

        if specentry.specification.active is False:
            messages.warning(self.request, _("Not active"))
            return reverse_lazy("shop:shopView")

        if specentry.specification.item.pk is not entry.item.pk:
            messages.warning(self.request, _("Not related specification"))
            return reverse_lazy("shop:shopView") 

        cart = Cart(self.request)
        cart.spec(entry.pk, specentry.pk)  

        messages.success(self.request, _('Cart was updated.'))
        return reverse_lazy("shop:shopView")       

class ItemListView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Item
    template_name = "adminItemList.html"
    permission_required = "shop.view_item"

class ItemDetailView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Item
    template_name = "adminItemDetail.html"
    permission_required = "shop.view_item"

    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
        context['priceHistory'] = Price.objects.filter(item=context['item']).order_by('till')

        return context

class ItemDeactivateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, RedirectView):

    permanent = False
    permission_required = "shop.update_item"

    def get_redirect_url(self, *args, **kwargs):
        if kwargs.get('pk', None) is None:
            messages.warning(self.request, _("Unknown key"))
            return reverse_lazy("shop:adminItemList")

        item = Item.objects.filter(pk = kwargs.get('pk')).first()
        if not item:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy("shop:adminItemList")

        price = item.price
        price.till = timezone.now()
        price.save()

        messages.success(self.request, _('Item deactivated'))
        return reverse_lazy("shop:adminItemList")

class ItemDeleteView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, RedirectView):

    permanent = False
    permission_required = "shop.delete_item"

    def get_redirect_url(self, *args, **kwargs):
        if kwargs.get('pk', None) is None:
            messages.warning(self.request, _("Unknown key"))
            return reverse_lazy("shop:adminItemList")

        item = Item.objects.filter(pk = kwargs.get('pk')).first()
        if not item:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy("shop:adminItemList")

        if item.price:
            messages.warning(self.request, _("Can not delete active items"))
            return reverse_lazy("shop:adminItemList")

        item.delete()
        messages.success(self.request, _('Item deleted'))
        return reverse_lazy("shop:adminItemList")

class ItemCreateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, FormView):

    form_class = ItemCreateForm
    template_name = "adminItemCreate.html"
    success_url = reverse_lazy("shop:adminItemList")
    permission_required = "shop.add_item"

    def form_valid(self, form):
        item = Item.objects.create(name=form.cleaned_data['name'], desc=form.cleaned_data['desc'], image=form.cleaned_data['image'])
        Price.objects.create(price=form.cleaned_data['price'], item=item, since=timezone.now(), till=form.cleaned_data['till'])

        if form.cleaned_data['specificationname'] != '' and form.cleaned_data['specificationvalue'] != '':
            specification = Specification.objects.create(name=form.cleaned_data['specificationname'], item=item, active=True)
            entries = form.cleaned_data['specificationvalue'].split(',')
            for entry in entries:
                SpecificationEntry.objects.create(value=entry, specification=specification)

        return super().form_valid(form)

class ItemUpdateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Item
    form_class = ItemUpdateForm
    template_name = "adminItemUpdate.html"
    success_url = reverse_lazy("shop:adminItemList")
    permission_required = "shop.change_item"

    def get_initial(self):
        initial = super(ItemUpdateView, self).get_initial()
        if self.object.price is not None:
            initial['price'] = self.object.price.price
            initial['till'] = self.object.price.till

        if self.object.specification is not None:
            initial['specificationname'] = self.object.specification.name
            initial['specificationvalue'] = ",".join(entry.value for entry in self.object.specification.entry)
                
        return initial

    def form_valid(self, form):
        if self.object.specification is not None:
            spec = self.object.specification
            spec.active=False
            spec.save()

        if form.cleaned_data['specificationname'] != '' and form.cleaned_data['specificationvalue'] != '':
            specification = Specification.objects.create(name=form.cleaned_data['specificationname'], item=self.object, active=True)
            entries = form.cleaned_data['specificationvalue'].split(',')
            for entry in entries:
                SpecificationEntry.objects.create(value=entry, specification=specification)

        if self.object.price is None:
            Price.objects.create(price=form.cleaned_data['price'], item=self.object, since=timezone.now(), till=form.cleaned_data['till'])

        if self.object.price is not None and ( self.object.price.price != form.cleaned_data['price'] or self.object.price.till != form.cleaned_data['till']):
            price = self.object.price
            price.till = timezone.now()
            price.save()

            Price.objects.create(price=form.cleaned_data['price'], item=self.object, since=timezone.now(), till=form.cleaned_data['till'])

        return super().form_valid(form)

class ItemCreateAsView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Item
    form_class = ItemCreateForm
    template_name = "adminItemCreate.html"
    success_url = reverse_lazy("shop:adminItemList")
    permission_required = "shop.add_item"

    def get_initial(self):
        initial = super(ItemCreateAsView, self).get_initial()
        if self.object.price is not None:
            initial['price'] = self.object.price.price
            initial['till'] = self.object.price.till

        if self.object.specification is not None:
            initial['specificationname'] = self.object.specification.name
            initial['specificationvalue'] = ",".join(entry.value for entry in self.object.specification.entry)
                
        return initial

    def form_valid(self, form):
        valid = super().form_valid(form)

        item = Item.objects.create(name=form.cleaned_data['name'], desc=form.cleaned_data['desc'], image=form.cleaned_data['image'])
        Price.objects.create(price=form.cleaned_data['price'], item=item, since=timezone.now(), till=form.cleaned_data['till'])

        if form.cleaned_data['specificationname'] != '' and form.cleaned_data['specificationvalue'] != '':
            specification = Specification.objects.create(name=form.cleaned_data['specificationname'], item=item, active=True)
            entries = form.cleaned_data['specificationvalue'].split(',')
            for entry in entries:
                SpecificationEntry.objects.create(value=entry, specification=specification)

        return valid

class OrderListView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = Order
    template_name = "adminOrderList.html"
    permission_required = "shop.view_order"

class OrderListUserView(LoginMixinView, LoginRequiredMixin, ListView):

    model = Order
    template_name = "userOrderList.html"

    def get_context_data(self, **kwargs):
        context = super(OrderListUserView, self).get_context_data(**kwargs)
        context['object_list'] = Order.objects.filter(user=self.request.user).all()

        return context

class OrderCreateView(LoginMixinView, FormView):

    template_name = "orderCreate.html"
    form_class = OrderCreateForm
    success_url = reverse_lazy("shop:shopView")

    def get_initial(self):
        initial = super(OrderCreateView, self).get_initial()
        if not self.request.user.is_anonymous:
            user = self.request.user
            initial['firstname'] = user.profile.name
            initial['lastname'] = user.profile.surname
            initial['email'] = user.email
            initial['city'] = user.profile.city
            initial['street'] = user.profile.address
            initial['post'] = user.profile.postalCode
            initial['phone'] = user.profile.phone

        return initial

    def render_to_response(self, context):
        cart = Cart(self.request)

        if cart.is_empty():
            messages.warning(self.request, _("Cart empty"))
            return redirect(reverse('shop:shopView'))

        if cart.is_valid() is False:
            messages.warning(self.request, _("Missing specification"))
            return redirect(reverse('shop:shopView'))

        return super(OrderCreateView, self).render_to_response(context)

    def form_valid(self, form):
        cart = Cart(self.request)

        if cart.is_empty():
            messages.warning(self.request, _("Cart empty"))
            return redirect(reverse('shop:shopView'))

        try:
            with transaction.atomic():
                if self.request.user:
                    form.instance.user = self.request.user
                form.instance.save()
                cart.attach(form.instance)

                yearVariableSymbol = ( datetime.datetime.now().year * 1000000 ) % 10000000000
                orderVariableSymbol = ( form.instance.pk * 15 + ( random.randint(0, 14))) % 1000000
                variableSymbol = yearVariableSymbol + orderVariableSymbol
                specificSymbol = 0

                Payment.objects.create(received=False, variableSymbol=variableSymbol, specificSymbol=specificSymbol, order=form.instance)

                message = render_to_string('orderEmail.html', {
                    'domain': get_current_site(self.request).domain,
                    'slug': form.instance.slug,
                    'vs': variableSymbol,
                    'ss': specificSymbol,
                    'account': ESHOP_BANK_ACCOUNT,
                    'cart': cart.cart
                })

                subject = "" + str(_("Order number")) + ": " + str(form.instance.pk) + " " + str(_("succesfully created"))
                text_content = ""
                msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [str(form.instance.email)])
                msg.attach_alternative(message, "text/html")
                msg.send()


        except Exception as e:
            print(e)
            messages.warning(self.request, _("Order can not be created now, please try again later"))
            return redirect(reverse('shop:shopView'))

        cart.detach(self.request)
        messages.success(self.request, _("Order was created. Mail with payment info was sent to your email address."))
        return super(OrderCreateView, self).form_valid(form)

class OrderPaymentConfirmView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, RedirectView):

    permanent = False
    permission_required = "shop.update_payment"

    def get_redirect_url(self, *args, **kwargs):
        paymentPK = kwargs.get('pk', None)
        if paymentPK is None:
            messages.warning(self.request, _("Unknown key"))
            return reverse_lazy('shop:adminOrderList')

        order = Order.objects.filter(pk=paymentPK).first()
        if not order:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy('shop:adminOrderList')

        payment = order.payment
        payment.received = True
        payment.save()

        messages.success(self.request, _("Order paid"))
        return reverse_lazy('shop:adminOrderList')

class OrderPaymentRevokeView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, RedirectView):

    permanent = False
    permission_required = "shop.update_payment"

    def get_redirect_url(self, *args, **kwargs):
        paymentPK = kwargs.get('pk', None)
        if paymentPK is None:
            messages.warning(self.request, _("Unknown key"))
            return reverse_lazy('shop:adminOrderList')

        order = Order.objects.filter(pk=paymentPK).first()
        if not order:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy('shop:adminOrderList')

        payment = order.payment
        payment.received = False
        payment.save()

        messages.success(self.request, _("Order paid"))
        return reverse_lazy('shop:adminOrderList')

class OrderTrackerView(LoginMixinView, TemplateView):

    template_name = "orderTracker.html"

    def dispatch(self, request, *args, **kwargs):
        orderSlug = kwargs.get('slug', None)
        if orderSlug is None:
            messages.warning(self.request, _("Unknown key"))
            return redirect(reverse('shop:shopView'))

        order = Order.objects.filter(slug=orderSlug).first()
        if not order:
            messages.warning(self.request, _("Not found"))
            return redirect(reverse('shop:shopView'))

        return super(OrderTrackerView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderTrackerView, self).get_context_data(**kwargs)
        context['order'] = Order.objects.filter(slug = kwargs['slug']).first()

        return context

class OrderDetailView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, DetailView):

    model = Order
    template_name = "adminOrderDetail.html"
    permission_required = "shop.view_order"