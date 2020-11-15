from django.shortcuts import render
from django.views.generic import ListView

from ..core.views import LoginMixinView
from .models import Item, Cart

class ShopIndex(LoginMixinView, ListView):

    model = Item
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        context = super(ShopIndex, self).get_context_data(**kwargs)
        
        cartdata = self.request.session.get('cart', Cart().memory)
        self.request.session['cart'] = cartdata

        # Validate cart

        context['cart'] = cartdata
        return context