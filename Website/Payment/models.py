from django.db import models
from django.contrib.auth.models import User
from Store.models import Product
from django.db.models.signals import post_save

# Create your models here.


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_full_name = models.CharField(max_length=100)
    shipping_email = models.CharField(max_length=255)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255 , null=True , blank=True)
    shipping_city = models.CharField(max_length=255)
    shipping_country = models.CharField(max_length=255)
    shipping_state = models.CharField(max_length=255 , null=True , blank=True)
    shipping_zipcode = models.CharField(max_length=255 , null=True , blank=True)


    # Dont Pluralize address
    class Mata:
        verbose_name_plural = 'Shipping Address bos'


    def __str__(self):
        return f' Shipping Address - {str(self.user)}'



# Create Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True , blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=255)
    shipping_address = models.CharField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=0)
    date_ordered = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{str(self.id)} - {self.full_name}'



# Create Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True , blank=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f'{str(self.id)}'







# Create a User Shipping Address by default when user sign up
def Create_Shipping_Address(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()


#Automate the profile thing
post_save.connect(Create_Shipping_Address, sender=User)