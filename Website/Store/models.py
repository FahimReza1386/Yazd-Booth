from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'uploads/category/' , null=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Booth(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/booth/', null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def like_count(self):
        return self.likes.count()

    def products(self):
        return self.product_set.all()

    def __str__(self):
        return self.name

class Like(models.Model):
    booth = models.ForeignKey(Booth, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('booth', 'user')

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
    Discountـpercentage = models.IntegerField(default=0)
    colors = models.ManyToManyField(Color) # انتخاب به صورت چند به چند
    features = models.ManyToManyField(Feature , default='')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE , null=True , related_name='products' , blank=False , default='' )



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
    user = models.ForeignKey(User, on_delete=models.CASCADE , default=None , null=False , blank=False)
    image = models.ImageField(upload_to='uploads/comments/')
    star = models.IntegerField(default=0)
    description = models.TextField(max_length=300 , default='' , null=True , blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.product}'


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , default=None , null=False , blank=False)
    image = models.ImageField(upload_to='uploads/profile/' , default='uploads/profile/user.ico')
    date_modified = models.DateTimeField(User , auto_now=True)
    phone = models.CharField(max_length=14 , blank=True)
    address1 = models.CharField(max_length=200 , blank=True)
    address2 = models.CharField(max_length=200 , blank=True)
    city = models.CharField(max_length=200 , blank=True)
    state = models.CharField(max_length=200 , blank=True)
    zipcode = models.CharField(max_length=200 , blank=True)
    country = models.CharField(max_length=200 , blank=True)
    melicode = models.CharField(max_length=200 , blank=True)
    role = models.CharField(max_length=200 , blank=True , default='Customer')
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE , null=True , blank=False , default=None)

    def __str__(self):
        return self.user.username


# Create a User Profile by default when user sign up
def Create_Profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


#Automate the profile thing
post_save.connect(Create_Profile, sender=User)