from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, OrderItem
from .cart import Cart
from django.urls import reverse
from .forms import Select_Quantity_Form, Fill_Data_Form


### returning products ids which are in the cart ###
def product_ids(cart):
    products_in_cart = []
    for item in cart:
        products_in_cart.append(int(item['product'].id))
    return products_in_cart
###################################################

def show_products(request):
    products = Product.objects.all()
    cart = Cart(request)
    products_in_cart = product_ids(cart)
    return render(request,'list_products.html',{'products':products,'products_in_cart':products_in_cart})

def product_detail(request,id):
    product = get_object_or_404(Product,pk=id)
    cart = Cart(request)
    form = Select_Quantity_Form()
    products_in_cart = product_ids(cart)
    return render(request,'product_detail.html',{'product':product,'products_in_cart':products_in_cart,'form':form})


def cart_add(request,id):
    product = get_object_or_404(Product,pk=id)
    cart = Cart(request)

    form = Select_Quantity_Form(request.POST)
    if form.is_valid():
        selected_quantity = form.cleaned_data['select_quantity']
        cart.add_to_cart(product=product,quantity=selected_quantity,update_quantity=True)
    from_path = request.META['HTTP_REFERER']
    if 'product_detail' in from_path:
        return redirect(reverse('product_detail', kwargs={"id": id}))
    elif 'cart_summary' in from_path:
        return redirect('cart_summary')
    else:
        cart.add_to_cart(product=product)
        return redirect('show_products')

def cart_remove(request,id):
    product = get_object_or_404(Product,pk=id)
    cart = Cart(request)
    cart.remove_from_cart(product=product)
    return redirect('cart_summary')

def cart_summary(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity'] = Select_Quantity_Form(initial={'select_quantity':item['quantity']})
    form = Select_Quantity_Form()
    return render(request,'cart_summary.html',{'cart':cart,'form':form})

def shipping_form(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = Fill_Data_Form(request.POST)
        order = form.save()
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],quantity=item['quantity'],price=item['price'])
        cart.clear()
        request.session['order_id'] = order.id
        return render(request,'order_success.html',{'cart':cart,'total_items':0,'order_id':order.id})
    else:
        form = Fill_Data_Form()

    return render(request,'shipping_form.html',{'form':form})


