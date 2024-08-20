from django.shortcuts import render,HttpResponse
from Cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress
# Create your views here.


def Test(request):
    return HttpResponse('Hi Im Testing ...')


def CheckOut_Order(request):
    # Get The Cart
    cart = Cart(request)

    product = cart.get_prods
    quants = cart.get_quants
    total = cart.get_total

    if request.user.is_authenticated:
        #Get The Modal Form
        current_user=ShippingAddress.objects.get(user_id=request.user.id)

        # Get The Shipping Form
        shipping_form = ShippingForm(request.POST or None , instance=current_user)
        return render(request=request,template_name='Checkout_Order.html' ,context={'products':product , 'quants':quants , 'total':total , 'shipping_form':shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request=request,template_name='Checkout_Order.html' ,context={'products':product , 'quants':quants , 'total':total , 'shipping_form':shipping_form})
