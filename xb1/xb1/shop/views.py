from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.base import RedirectView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.core import serializers
from django.utils import timezone

from ..core.views import LoginMixinView
from .models import Item, Price, CartEntry
from .cart import Cart
from .forms import ItemCreateForm, ItemUpdateForm

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
        if item is None:
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
        if entry is None:
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
        if entry is None:
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
            if entry is None:
                messages.warning(self.request, _("Not found"))
                return reverse_lazy("shop:shopView")

            cart = Cart(self.request)
            cart.discard(entry.pk)

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

class ItemCreateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, FormView):

    form_class = ItemCreateForm
    template_name = "adminItemCreate.html"
    success_url = reverse_lazy("shop:adminItemList")
    permission_required = "shop.add_item"

    def form_valid(self, form):
        item = Item.objects.create(name=form.cleaned_data['name'], desc=form.cleaned_data['desc'], image=form.cleaned_data['image'])
        Price.objects.create(price=form.cleaned_data['price'], item=item, since=timezone.now(), till=form.cleaned_data['till'])

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
        return initial

    def form_valid(self, form):
        if self.object.price is None:
            Price.objects.create(price=form.cleaned_data['price'], item=self.object, since=timezone.now(), till=form.cleaned_data['till'])

        if self.object.price is not None and ( self.object.price.price != form.cleaned_data['price'] or self.object.price.till != form.cleaned_data['till']):
            price = self.object.price
            price.till = timezone.now()
            price.save()

            Price.objects.create(price=form.cleaned_data['price'], item=self.object, since=timezone.now(), till=form.cleaned_data['till'])

        return super().form_valid(form)