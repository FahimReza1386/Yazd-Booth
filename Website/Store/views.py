from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm , UpdateUserProfile
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


def Update_User(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserProfile(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request , 'تبریک ! پروفایل شما با موفقیت تغییر کرد ...')
            return redirect('/')

        return render(request=request , template_name='Update_Profile.html' , context={'user_form':user_form})
    else:
        messages.success(request , 'لطفا قبل از تغییر پروفایل با حساب کاربری خود وارد شوید ...')
        return redirect('/')

def Product_Page(request , id):
    product= Product.objects.filter(id=id).all()
    comment=Comments.objects.filter(product=id).all()
    return render(request=request , template_name='Product.html' , context={'product':product , 'comment':comment})


def Category_Page(request , foo):
    foo1 = foo.replace('-' , ' ')
    try:
        category = Category.objects.get(name=foo1)
        product=Product.objects.filter(category=category)
        return render(request=request , template_name='Category.html' , context={'product':product})
    except:
        messages.success(request , "این دسته بندی وجود ندارد ...")
        return redirect('/')