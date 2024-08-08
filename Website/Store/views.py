from django.shortcuts import render,HttpResponse
from .models import *


# Create your views here.


def Home(request):
    products=Product
    return render(request=request , template_name='Home.html' , context={'products':products})