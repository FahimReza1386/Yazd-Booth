from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


# Create your views here.


def Home(request):
    products=Product.objects.all()
    booth= Booth.objects.all()
    category = Category.objects.all()
    return render(request=request , template_name='Home.html' , context={'Product':products ,'Booth':booth , 'category':category})


def About(request):
    return render(request=request , template_name='About.html' , context={})

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'تبریک ! با موفقیت به حساب خود وارد شدید ...')
            return redirect('/')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور معتبر نیست ...')
            return redirect('Login')
    else:
        return render(request=request, template_name='Login.html', context={})

def Logout(request):
    logout(request)
    messages.success(request, 'با موفقیت از حساب خود خارج شدید ...')
    return redirect('/')


def Register(request):
    if request.method == "POST":
        forms = RegisterForm(request.POST)
        users = User.objects.filter(username=forms.data['username']).all()
        if len(users)<=0:
            if forms.is_valid():
                if forms.data['password1'] == forms.data['password2']:
                    forms.save()
                    username = forms.data['username']
                    password2 = forms.data['password2']
                    user = authenticate(username=username, password=password2)
                    if user is not None:
                        login(request, user)
                        messages.success(request , 'حساب کاربری شما با موفقیت ساخته شد ...')
                        return redirect('/')
                else:
                    messages.success(request , "اختطار ! رمز عبور ها با یکدیگر متفاوت اند ..")
                    return redirect('Register')
            else:
                messages.error(request, 'فیلد های وارد شده اشتباه میباشد ...')
                return redirect('/')
        else:
            messages.success(request, 'نام کاربری وجود دارد ...')
            return redirect('Register')

    else:
        forms = RegisterForm()
        return render(request=request , template_name='Register.html' , context={'form':forms})



def Product_Page(request , id):
    product= Product.objects.filter(id=id).all()
    comment=Comments.objects.filter(product=id).all()

    return render(request=request , template_name='Product.html' , context={'product':product , 'comment':comment})