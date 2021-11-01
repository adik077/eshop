from django.urls import path
from .views import show_products,product_detail, cart_add,cart_remove,cart_summary,shipping_form

urlpatterns = [
    path('', show_products,name='show_products'),
    path('product_detail/<int:id>', product_detail,name='product_detail'),
    path('cart_add/<int:id>',cart_add,name='cart_add'),
    path('cart_remove/<int:id>',cart_remove,name='cart_remove'),
    path('cart_summary',cart_summary,name='cart_summary'),
    path('shipping_form',shipping_form,name='shipping_form'),
]
