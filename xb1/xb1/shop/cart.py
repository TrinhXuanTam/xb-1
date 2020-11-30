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

    def insert(self, item):
        specification = item.specification.entry.first() if item.specification else None
        models.CartEntry.objects.create(cart=self.cart, item=item, count=1, price=item.price, specification=specification)

    def add(self, pk, count=1):
        entry = models.CartEntry.objects.filter(cart=self.cart, pk=pk).first()
        if entry:
            entry.count += count
            entry.price = entry.item.price
            entry.save()

    def spec(self, pk, specpk):
        entry = models.CartEntry.objects.filter(cart=self.cart, pk=pk).first()
        spec = models.SpecificationEntry.objects.filter(pk=specpk).first()
        if entry and spec:
            entry.specification = spec
            entry.save()

    def remove(self, pk, count=1):
        entry = models.CartEntry.objects.filter(cart=self.cart, pk=pk).first()
        if entry:
            entry.count -= count
            if entry.count < 1:
                entry.cart = None
                entry.delete()
            else:    
                entry.price = entry.item.price
                entry.save()

    def discard(self, pk):
        if pk is None:
            for entry in self.cart.cartentry_set.all():
                entry.count = 0
                entry.cart = None
                entry.delete()
        else:    
            entry = models.CartEntry.objects.filter(cart=self.cart, pk=pk).first()
            entry.count = 0
            entry.cart = None
            entry.delete()

    def is_empty(self):
        if models.CartEntry.objects.filter(cart=self.cart):
            return False
        else:
            return True

    def is_valid(self):
        for entry in self.cart.cartentry_set.all():
            if entry.item.specification is None:
                continue

            if entry.item.specification is not None and entry.specification is None:
                return False
            
            if entry.item.specification.pk is not entry.specification.specification.pk:
                return False
        return True

    def attach(self, order):
        self.cart.order = order
        self.cart.save()

    def detach(self, request):
        del request.session[CART_KEY]