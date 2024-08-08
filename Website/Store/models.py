from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booth(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/booth' , max_length=5)
    likes = models.IntegerField(default=0)
    Owner=models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=100 , null=False , blank=False)
    last_name = models.CharField(max_length=100 , null=False , blank=False)
    phone = models.CharField(max_length=100 , null=True)
    meli_code = models.CharField(max_length=100 , null=True)
    postal_code = models.CharField(max_length=100 , null=True)
    username = models.CharField(max_length=100 , null=False , blank=False)
    password1 = models.CharField(max_length=100 , null=False , blank=False)
    password2 = models.CharField(max_length=100 , null=False , blank=False)


    def __str__(self):
        return f'{self.last_name} {self.meli_code}'


class Product(models.Model):
    name = models.CharField(max_length=100 , null=False , blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=0 , default=0 , null=False , blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , default=None , null=False , blank=False)
    description = models.TextField(max_length=300 , default='' , null=True , blank=True)
    image = models.ImageField(upload_to='uploads/product/')
    is_active = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    sale_price = models.IntegerField(default=0)
    colors = models.ManyToManyField(Color) # انتخاب به صورت چند به چند


    def __str__(self):
        return self.name




class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE , default=None , null=False , blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE , default=None , null=False , blank=False)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=11 , default='')
    date_ordered = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.customer} {self.product}'



class Comments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , default=None , null=False , blank=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE , default=None , null=False , blank=False)
    image = models.ImageField(upload_to='uploads/comments/')
    star = models.IntegerField(default=0)
    description = models.TextField(max_length=300 , default='' , null=True , blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.product}'