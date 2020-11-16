from django.utils import timezone

from . import models

CART_KEY = "cart"

class Cart:
    def __init__(self, request):
        cartPk = request.session.get(CART_KEY)
        if cartPk:
            cart = models.Cart.objects.filter(pk=cartPk, order=None).first()
            if cart is None:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart
        self.validate()

    def __iter__(self):
        for item in self.cart.cartentry_set.all():
            yield item

    def validate(self):
        price = 0
        for entry in self.cart.cartentry_set.all():
            price += entry.price.price * entry.count
        self.price = price
        self.count = self.cart.cartentry_set.all().count

    def new(self, request):
        cart = models.Cart.objects.create(creation=timezone.now())
        request.session[CART_KEY] = cart.pk
        request.session.modified = True

        return cart

    def add(self, item, count=1):
        entry = models.CartEntry.objects.filter(cart=self.cart, item=item).first()
        if entry:
            entry.count += count
            entry.price = entry.item.price
            entry.save()
        else:
            models.CartEntry.objects.create(cart=self.cart, item=item, count=count, price=item.price)

    def remove(self, item, count=1):
        entry = models.CartEntry.objects.filter(cart=self.cart, item=item).first()
        if entry:
            entry.count -= count
            if entry.count < 1:
                entry.cart = None
                entry.delete()
            else:    
                entry.price = entry.item.price
                entry.save()

    def discard(self, item):
        if item is None:
            for entry in self.cart.cartentry_set.all():
                entry.count = 0
                entry.cart = None
                entry.delete()
        else:    
            entry = models.CartEntry.objects.filter(cart=self.cart, item=item).first()
            entry.count = 0
            entry.cart = None
            entry.delete()