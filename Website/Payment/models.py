from django.db import models
from django.contrib.auth.models import User


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
