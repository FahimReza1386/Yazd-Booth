from django import  forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name =forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder': 'نام و نام خانوادگی :'}), max_length=100)
    shipping_email = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder': 'ایمیل :'}), max_length=100)
    shipping_address1 = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder': 'ادرس اول :'}), max_length=100)
    shipping_address2 = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder': 'ادرس دوم (اختیاری) :'}), max_length=100)
    shipping_city = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder': 'شهر :'}), max_length=100)
    shipping_country = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder': 'کشور :'}), max_length=100)
    shipping_zipcode = forms.CharField(required=False,label='', widget=forms.TextInput(attrs={'placeholder': 'کدپستی :'}), max_length=100)


    class Meta:
        model = ShippingAddress
        fields = ('shipping_full_name' , 'shipping_email' , 'shipping_address1' , 'shipping_address2' , 'shipping_city' , 'shipping_country' , 'shipping_zipcode' )

        exclude = ['user' ,]


