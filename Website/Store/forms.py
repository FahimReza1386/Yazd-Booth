from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , SetPasswordForm
from django import forms

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
