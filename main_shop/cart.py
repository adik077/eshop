from decimal import Decimal

from django.conf import settings
from .models import Product

class Cart(object):
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart=cart


    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item



    def add_to_cart(self,product,quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]={'price':str(product.price),'quantity':0}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove_from_cart(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True


    def total_items(self):
        sum=0
        for item in self.cart.values():
            sum=sum+item['quantity']
        return sum

    def get_total_price(self):
        sum=0
        for item in self.cart.values():
            sum=sum+item['quantity']*Decimal(item['price'])
        return sum


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


    def draw_products(self):
        return self.cart