from django.shortcuts import render,HttpResponse,redirect
from Cart.cart import Cart
from .forms import ShippingForm , PaymentForm
from .models import ShippingAddress
from django.contrib import messages
# Create your views here.

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


def Billing_Info(request):
    if request.user.is_authenticated:
        if request.POST:
            # Get The Cart
            cart = Cart(request)

            product = cart.get_prods
            quants = cart.get_quants
            total = cart.get_total

            # Get The Billing Form
            billing_form = PaymentForm()

            return render(request=request , template_name="Billing_Info.html" , context={'products':product , 'quants':quants , 'total':total , 'shipping_info':request.POST , 'billing_form':billing_form})
        else:
            messages.success(request, "خطای دسترسی ...")
            return redirect('/')
    else:
        messages.success(request , "لطفا اول با حساب کاربری خود وارد شوید ...")
        return redirect('/')