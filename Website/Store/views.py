from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm , UpdateUserProfile ,UpdatePasswordForm , UpdateInfo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import jdatetime
from django.db.models import Count , Q
from Cart.cart import Cart
from Payment.forms import ShippingForm
from Payment.models import ShippingAddress
from datetime import datetime
import json
from django.contrib import messages



# Create your views here.


def Home(request):
    booth= Booth.objects.all()
    category = Category.objects.all()
    prd_last = Product.objects.order_by('-created_at')[:5]
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
            return render(request=request, template_name='Home.html',context={'Product': prd_last, 'Booth': booth, 'category': category, 'user': user,'search': searched })
    else:
        return render(request=request , template_name='Home.html' , context={'Product':prd_last ,'Booth':booth , 'category':category , 'user':user })

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


def Update_Info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user=Profile.objects.get(user__id=request.user.id)
        # Get Current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get original User Form
        forms = UpdateInfo(request.POST or None , request.FILES or None , instance=current_user)
        # Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None , instance=shipping_user)

        if forms.is_valid() or shipping_form.is_valid():
            # Save original Form
            forms.save()
            # Save Shipping Form
            shipping_form.save()

            messages.success(request , 'اطلاعات شما با موفقیت تغییر کرد ...')
            return redirect('/')
        else:
            for error in list(forms.errors.values()) and list(shipping_form.errors.values()):
                messages.error(request , error)
                return redirect('Update_Info')

        return render(request=request , template_name='Update_Info.html' , context={'forms':forms , 'shipping_form' : shipping_form})

    else:
        messages.error(request , 'لطفا قبل از هر اقدامی با حساب کاربری خود وارد شوید ...')
        return redirect('/Login')

def Product_Page(request , id):
    product= Product.objects.filter(id=id).all()
    comment=Comments.objects.filter(product=id).all()
    FeatureـProducts=FeatureـProduct.objects.filter(product=id).all()
    color=Color.objects.filter(prd=id).all()
    return render(request=request , template_name='Product.html' , context={'product':product , 'comment':comment , 'Feature':FeatureـProducts , 'color':color })


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
            if item.role == 'Boother':
                if item.booth.date_created:
                    g_date = item.booth.date_created  # تاریخ میلادی از نمونه
                    j_date = jdatetime.datetime.fromgregorian(datetime=g_date)  # تبدیل به تاریخ شمسی
                    formatted_date = f"{j_date.year}/{j_date.month}/{j_date.day}"

            else:
                formatted_date = 'None'

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


def Add_Product(request):
    if request.user.is_authenticated:
        curren_user=Profile.objects.get(user=request.user)
        role= curren_user.role
        if role == 'Boother':
            if request.method == 'POST':
                name = request.POST.get('name')
                images = request.FILES.get('img')
                description = request.POST.get('description')
                price = request.POST.get('price')
                discount_sale = request.POST.get('sale_price')
                category = request.POST.get('category')
                feature_name = request.POST.get('featureـname')
                feature_value = request.POST.get('feature_value')
                color = request.POST.get('color')
                try:
                    Cat_Instanse = Category.objects.get(name=category)
                    boothes = Booth.objects.filter(owner=request.user)

                    if not boothes.exists():
                        messages.error(request, 'شما هیچ غرفه‌ای ندارید.')
                        return redirect('Add_Product')

                    booth = boothes.first()

                    prd = Product(
                        name=name,
                        category=Cat_Instanse,
                        description=description,
                        price=price,
                        Discountـpercentage=discount_sale,
                        image=images,
                        booth=booth
                    )

                    if images and images.content_type in ['image/jpeg', 'image/png', 'image/webp', 'image/jpg']:
                        prd.image=images
                    else:
                        messages.error(request , 'لطفا یک عکس را وارد کنید ..')
                        return redirect('Add_Product')
                    prd.save()

                    # اضافه کردن رنگ‌ها به فیلد many-to-many
                    color_objects = Color(name=color , prd=prd)
                    color_objects.save()

                    # اضافه کردن ویژگی‌ها به فیلد many-to-many
                    features = FeatureـProduct(product=prd , feature_name=feature_name , feature_value=feature_value)
                    features.save()

                    messages.success(request, 'سلام غرفه دار گرامی محصول شما با موفقیت ثبت شد ...')
                    return redirect('Home')

                except Category.DoesNotExist:
                    messages.error(request, 'سلام دوست گرامی متاسفانه این دسته بندی وجود ندارد ...')
                    return redirect('Add_Product')
                # except Exception as e:
                #     messages.error(request, f'خطا در ذخیره محصول: {str(e)}')
                #     return redirect('Add_Product')
            else:
                return render(request=request, template_name='CreateProduct.html', context={})
        else:
            messages.error(request , "ثبت محصول تنها برای غرفه داران میباشد ...")
            return redirect('Customer_UserPanel')

    else:
        messages.error(request, 'لطفاً ابتدا وارد حساب کاربری خود شوید.')
        return redirect('Login')