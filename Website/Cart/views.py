from django.shortcuts import render , get_object_or_404
from .cart import Cart
from Store.models import Product
from django.http import JsonResponse
# Create your views here.
def Cart_Summary(request):
    return render(request=request, template_name='Cart_Summary.html' , context={})

def Cart_Add(request):

    # Get The Cart
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        #Get stuff
        product_id=int(request.POST.get('product_id'))

        # Lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save To Session
        cart.add(product=product)

        # Get The Cart Quantity
        cart_quantity=cart.__len__()


        # Return response
        response = JsonResponse({'qty ' : cart_quantity})
        return response


def Cart_Delete(request):
    pass

def Cart_Update(request):
    pass