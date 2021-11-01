from .cart import Cart

def cart_context(request):
    cart = Cart(request)
    total_items = cart.total_items()
    total_price = cart.get_total_price()
    return {'cart':cart,'total_items':total_items,'total_price':total_price,'request':request}
