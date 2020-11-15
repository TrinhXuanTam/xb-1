from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.core import serializers

from ..core.views import LoginMixinView
from .models import Item, Cart

class ShopIndex(LoginMixinView, ListView):

    model = Item
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        context = super(ShopIndex, self).get_context_data(**kwargs)
        
        cartdata = self.request.session.get('cart', [])
        self.request.session['cart'] = cartdata

        cart = Cart(cartdata)
        context['cart'] = cart.asTemplate()

        return context

class CartAddItemView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if kwargs.get('pk', None) is None:
            messages.warning(self.request, _("Unknown item ID"))
            return reverse_lazy("shop:shopView")

        item = Item.objects.filter(pk = kwargs.get('pk')).first()
        if item is None:
            messages.warning(self.request, _("Not found"))
            return reverse_lazy("shop:shopView")

        cart = Cart(self.request.session.get('cart', []))
        result = cart.add(item, 1)

        if result is not None:
            messages.warning(self.request, _(validationResult))
            return reverse_lazy("shop:shopView")

        self.request.session['cart'] = cart.memory
        self.request.session.modified = True

        messages.success(self.request, _('Cart was updated.'))
        return reverse_lazy("shop:shopView")