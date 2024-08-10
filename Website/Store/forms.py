from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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


