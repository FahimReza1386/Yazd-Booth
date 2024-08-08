from django.shortcuts import render,HttpResponse
from .models import *


# Create your views here.


def Home(request):
    products=Product.objects.all()
    booth= Booth.objects.all()
    category = Category.objects.all()
    return render(request=request , template_name='Home.html' , context={'Product':products ,'Booth':booth , 'category':category})

