from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm , UpdateUserProfile ,UpdatePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import jdatetime
from datetime import datetime

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
                forms.save()
                username = forms.data['username']
                password2 = forms.data['password2']
                user = authenticate(username=username, password=password2)
                if user is not None:
                    login(request, user)
                    messages.success(request , 'حساب کاربری شما با موفقیت ساخته شد ...')
                    return redirect('/')
            else:
                for error in list(forms.errors.values()):
                    if error[0] == 'The password is too similar to the username.':
                        messages.error(request, "رمز عبور بسیار شبیه به نام کاربری میباشد ...")
                        return redirect('Register')
                    elif error[0] == 'This password is too short. It must contain at least 8 characters.':
                        messages.error(request, "طول رمز عبور کوتاه میباشد . حداقل ۸ کاراکتر ...")
                        return redirect('Register')
                    elif error[0] == 'The two password fields didn’t match.':
                        messages.error(request, "رمز عبور و تکرار رمز عبور باید یکسان باشد ...")
                        return redirect('Register')
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



def Update_Password(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)

        if request.method == 'POST':
            form = UpdatePasswordForm(current_user , request.POST)

            if form.is_valid():
                form.save()
                messages.success(request , 'رمزعبور شما با موفقیت تغییر کرد ...')
                login(request, current_user)
                return redirect('Login')

            else:
                for error in list(form.errors.values()):
                    if error[0] == 'The password is too similar to the username.':
                        messages.error(request , "رمز عبور بسیار شبیه به نام کاربری میباشد ...")
                        return redirect('Update_Password')
                    elif error[0] == 'This password is too short. It must contain at least 8 characters.':
                        messages.error(request, "طول رمز عبور کوتاه میباشد . حداقل ۸ کاراکتر ...")
                        return redirect('Update_Password')
                    elif error[0] == 'The two password fields didn’t match.':
                        messages.error(request, "رمز عبور و تکرار رمز عبور باید یکسان باشد ...")
                        return redirect('Update_Password')
        else:
            form =UpdatePasswordForm(current_user)
            return render(request=request , template_name='Update_Password.html' , context={'form':form})
    else:
        messages.error(request , 'لطفا قبل از درخواست تغییر رمز ورود با حساب خود وارد شوید ...')
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


def Customer_UserPanel(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)
        for item in profile:

            # تاریخ ساخت غرفه
            if item.booth.date_created:
                g_date = item.booth.date_created  # تاریخ میلادی از نمونه
                j_date = jdatetime.datetime.fromgregorian(datetime=g_date)  # تبدیل به تاریخ شمسی
                formatted_date = f"{j_date.year}/{j_date.month}/{j_date.day}"

            # تغییر در حساب کاربری
            if item.date_modified:
                h_date = item.date_modified # تاریخ میلادی از نمونه
                f_date = jdatetime.datetime.fromgregorian(datetime=h_date)  # تبدیل به تاریخ شمسی

                # فرمت تاریخ شمسی
                # formatted_date2 = f"{f_date.year}/{f_date.month}/{f_date.day} ساعت {h_date.hour}:{h_date.minute}"

                formatted_date2 = f"{f_date.year}/{f_date.month}/{f_date.day}"



    else:
        messages.success(request , 'لطفا با حساب کاربری خود وارد شوید ...')
        return redirect('Login')
    return render(request=request , template_name='Customer_UserPanel.html' , context={'profile':profile , 'create_booth':formatted_date , 'date_modified':formatted_date2 })
