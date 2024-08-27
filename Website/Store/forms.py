from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , SetPasswordForm
from django import forms
from .models import Profile, Booth


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True,label='', widget=forms.TextInput(attrs={'placeholder':'نام :'}), max_length=100)
    last_name = forms.CharField(required=True,label='',widget=forms.TextInput(attrs={'placeholder':'نام خانوادگی :'}), max_length=100)
    username = forms.CharField(required=True,label='',widget=forms.TextInput(attrs={'placeholder':'نام کاربری :'}), max_length=100)
    password1 = forms.CharField(required=True,label='', widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور :'}))
    password2 = forms.CharField(required=True,label='', widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز عبور :'}))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username' , 'password1' , 'password2')




class UpdateUserProfile(UserChangeForm):
    # Password is Stuff
    password = None
    # Get Other Field
    username = forms.CharField(required=True,label='',widget=forms.TextInput(attrs={'placeholder':'نام کاربری :'}), max_length=100)
    first_name = forms.CharField(required=True,label='', widget=forms.TextInput(attrs={'placeholder':'نام :'}), max_length=100)
    last_name = forms.CharField(required=True,label='',widget=forms.TextInput(attrs={'placeholder':'نام خانوادگی :'}), max_length=100)
    email = forms.EmailField(required=True,label='',widget=forms.TextInput(attrs={'placeholder':'ایمیل :'}), max_length=100)

    class Meta:
        model = User
        fields = ('username' , 'first_name' , 'last_name' , 'email')



class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(required=True,label='', widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور :'}))
    new_password2 = forms.CharField(required=True,label='', widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز عبور :'}))


    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')



class UpdateInfo(forms.ModelForm):
    phone = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder':'تلفن همراه :'}), max_length=100)
    address1 = forms.CharField(required=False,label='',widget=forms.TextInput(attrs={'placeholder':'ادرس اول :'}), max_length=100)
    address2 = forms.CharField(required=False,label='',widget=forms.TextInput(attrs={'placeholder':'ادرس دوم (اختیاری) :'}), max_length=100)
    city = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder':'شهر :'}))
    country = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder':'کشور :'}))
    zipcode = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder':'کدپستی :'}))
    melicode = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder':'کدملی :'}))

    class Meta:
        model = Profile
        fields = ('phone' , 'address1', 'address2', 'city', 'country', 'zipcode', 'melicode' , 'image')

    def __str__(self):
        return self.phone





class CreateBoothForm(forms.ModelForm):
    name=forms.CharField(required=True , max_length=100 , label='',widget=forms.TextInput(attrs={'placeholder' : 'نام غرفه خود را وارد کنید ..'}))
    address=forms.CharField(required=True , max_length=100 , label='' , widget=forms.TextInput(attrs={'placeholder' : 'ادرس غرفه خود را وارد کنید ..'}))
    description=forms.CharField(required=True , max_length=100, label='' , widget=forms.TextInput(attrs={'placeholder' : 'توضیحات غرفه خود را وارد کنید ..'}))

    class Meta:
        model = Booth
        fields = ['name' , 'address' , 'description' , 'image']

