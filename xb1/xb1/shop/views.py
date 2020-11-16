from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.core import serializers

from ..core.views import LoginMixinView
from .models import Item, CartEntry
from .cart import Cart

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