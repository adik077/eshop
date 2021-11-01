from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import braintree
from main_shop.models import Order, OrderItem, Product
from .utils import render_invoice_to_pdf
from django.core.mail import EmailMessage

def payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    total_sum=sum(item.get_cost() for item in order_items)
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce',None)
        result = braintree.Transaction.sale({
            'amount':'{:.2f}'.format(total_sum),
            'payment_method_nonce':nonce,
            'options':{'submit_for_settlement':True}
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            ############# changing products quantity ###################
            for item in order_items:
                product = get_object_or_404(Product,id=item.product.id)
                difference = product.quantity-item.quantity
                if difference <= 0:
                    product.quantity = 0
                    product.is_available = False
                else:
                    product.quantity = product.quantity-item.quantity
                product.save()
            #############################################################
            ############ sending invoice by mail ########################
            data = {
                'order_number': order.id,
                'name': order.name,
                'surname': order.surname,
                'email': order.email,
                'phone': order.phone,
                'address': order.address,
                'post_code': order.post_code,
                'city': order.city,
                'order_items':order_items,
                'total_sum':total_sum,
            }
            mail_title = "E-shop Invoice {}".format(order.id)
            mail_body = "{},\n Thank You for shopping with us. Hope You are happy. Please find Your invoice as an attachment\n Best Regards,\n E-shop".format(order.name)
            pdf = render_invoice_to_pdf('pdf_invoice.html', context=data)
            email = EmailMessage(mail_title, mail_body, 'email@here.com', [order.email])
            email.attach('invoice.pdf', pdf.getvalue(), 'application/pdf')
            email.send()
            #############################################################
            return render(request,'Payment/payment_done.html',{})
        else:
            return render(request,'Payment/payment_failed.html',{})
    else:
        client_token = braintree.ClientToken.generate()
        return render(request,'Payment/payment.html',{'order':order,'client_token':client_token})





