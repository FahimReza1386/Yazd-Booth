from django.shortcuts import render,HttpResponse,redirect
from Cart.cart import Cart
from .forms import ShippingForm , PaymentForm
from .models import ShippingAddress , Order , OrderItem
from django.contrib.auth.models import User
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

            my_shipping=request.POST
            request.session['my_shipping']=my_shipping

            # Get The Billing Form
            billing_form = PaymentForm()

            return render(request=request , template_name="Billing_Info.html" , context={'products':product , 'quants':quants , 'total':total , 'shipping_info':request.POST , 'billing_form':billing_form})
        else:
            messages.success(request, "خطای دسترسی ...")
            return redirect('/')
    else:
        messages.success(request , "لطفا اول با حساب کاربری خود وارد شوید ...")
        return redirect('/Login')




def Process_Order(request):
    if request.POST:
        cart = Cart(request)

        products = cart.get_prods
        quants = cart.get_quants()
        totals = cart.get_total()

        # Get The Billing Info From The Last Page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping=request.session.get('my_shipping')

        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address From Session Info
        Shipping_Address = (f"{my_shipping['shipping_address1']} \n {my_shipping['shipping_address2']} \n {my_shipping['shipping_city']} \n {my_shipping['shipping_zipcode']} \n ")

        amount_paid=totals

        # Create an Order

        if request.user.is_authenticated:
            # Get The Cart

            # Logged In
            user = request.user
            #Create Order

            create_order=Order(user=user , full_name=full_name , email=email , shipping_address=Shipping_Address,amount_paid=amount_paid)
            create_order.save()

            # Create an Order-Items
            # Get The Order Id
            order_id = create_order.pk
            # Get Product Info
            for product in cart.get_prods():
                # Get Product Id
                product_id = product.id
                price = int(product.price)
                discount = int(product.Discountـpercentage) / 100
                # Get Product Price
                total = price - (price * discount)
                # Get The Quantity

                for key , value in quants.items():
                    if int(key) == product.id:
                        # Create Order Item
                        create_order_item = OrderItem(order_id=order_id, product_id=product.id , user=user , quantity=value ,price=total)
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            messages.success(request , 'سفارش شما با موفقیت ثبت شد ...')
            return redirect('/')


        else:
            messages.success(request, "لطفا اول با حساب کاربری خود وارد شوید ...")
            return redirect('/Login')
    else:
        messages.success(request, "خطای دسترسی ...")
        return redirect('/')