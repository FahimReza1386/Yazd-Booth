from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm , UpdateUserProfile ,UpdatePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import jdatetime
from django.db.models import Count , Q
from    Cart.cart import Cart
from datetime import datetime
import json
# Create your views here.


def Home(request):
    products=Product.objects.all()
    booth= Booth.objects.all()
    category = Category.objects.all()
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
    else:
        user=None

    if request.method == 'POST':
        searched = request.POST['search']
        # Query The Product DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test For NUll
        if not searched:
            messages.error(request , 'متاسفانه محصولی با این نام وحود ندارد ...')
            return render(request=request , template_name='Home.html' , context={})
        else:
            return render(request=request, template_name='Home.html',context={'Product': products, 'Booth': booth, 'category': category, 'user': user,'search': searched})
    else:
        return render(request=request , template_name='Home.html' , context={'Product':products ,'Booth':booth , 'category':category , 'user':user})

def Like_Booth(request):
    if request.method == 'POST':
        user=User.objects.get(username=request.POST['user'])
        booth=Booth.objects.get(id=request.POST['booth'])
        like, created = Like.objects.get_or_create(user=user, booth=booth)
        if created:
            like.save()

            booths = Booth.objects.annotate(likes_count=Count('likes'))
            total_likes = sum(booth.likes_count for booth in booths)
            if total_likes > 0:
                for booth in booths:
                    percentage = (booth.likes_count / total_likes) * 100
                    booth.popularity_percentage = round(percentage, 2)  # ذخیره درصد محبوبیت
                    booth.save()  # ذخیره تغییرات در دیتابیس

                # مرتب‌سازی بر اساس درصد محبوبیت
                popularity_percentages = sorted(
                    [(booth.name, booth.popularity_percentage) for booth in booths],
                    key=lambda x: x[1],
                    reverse=True
                )

            else:
                return JsonResponse('هیچ لایکی ثبت نشده')


            return redirect('Home')
        else:
            like.delete()

            booths = Booth.objects.annotate(likes_count=Count('likes'))
            total_likes = sum(booth.likes_count for booth in booths)
            if total_likes > 0:
                for booth in booths:
                    percentage = (booth.likes_count / total_likes) * 100
                    booth.popularity_percentage = round(percentage, 2)  # ذخیره درصد محبوبیت
                    booth.save()  # ذخیره تغییرات در دیتابیس

                # مرتب‌سازی بر اساس درصد محبوبیت
                popularity_percentages = sorted(
                    [(booth.name, booth.popularity_percentage) for booth in booths],
                    key=lambda x: x[1],
                    reverse=True
                )

            else:
                return JsonResponse('هیچ لایکی ثبت نشده')


            return redirect('Home')

    else:
        return redirect('Home')

def Check_Like(request):
    if request.method == 'GET':
        user = request.user
        liked_booths = Like.objects.filter(user=user).values_list('booth_id', flat=True)
        return JsonResponse({'likedBooths': list(liked_booths)})
    else:
        return redirect('Home')

def About(request):
    return render(request=request , template_name='About.html' , context={})

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Do Some Shipping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get Their Saved Cart From DataBase
            saved_cart = current_user.old_cart
            #Convert DataBase String To Python Dictionary
            if saved_cart:
                # Convert To Dictionary Using Json
                convert_cart = json.loads(saved_cart)
                # Add the loaded cart dictionary to our session
                # Get the cart
                cart = Cart(request)
                # Loop Thru The Cart And Add The Items From The DataBase
                for key,value in convert_cart.items():
                    cart.db_add(product=key , quantity=value)

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
