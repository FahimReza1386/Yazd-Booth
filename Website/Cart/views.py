from django.shortcuts import render , get_object_or_404
from .cart import Cart
from Store.models import Product
from django.http import JsonResponse
# Create your views here.
def Cart_Summary(request):
    cart = Cart(request)
    product = cart.get_prods
    quants = cart.get_quants

    return render(request=request, template_name='Cart_Summary.html' , context={'products':product , 'quants':quants})

def Cart_Add(request):

    # Get The Cart
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        #Get stuff
        product_id=int(request.POST.get('product_id'))
        product_qty=int(request.POST.get('product_qty'))

        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save To Session
        cart.add(product=product , quantity=product_qty)

        # Get The Cart Quantity
        cart_quantity=cart.__len__()


        # Return response
        response = JsonResponse({'qty ' : cart_quantity})
        return response


def Cart_Delete(request):
    pass

def Cart_Update(request):
    # get The Cart
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id=int(request.POST.get('product_id'))
        product_qty=int(request.POST.get('product_qty'))

        cart.update(product_id=product_id, quantity=product_qty)

        response = JsonResponse({'qty ' : product_qty})
        return response
        return redirect('Cart_Summary')