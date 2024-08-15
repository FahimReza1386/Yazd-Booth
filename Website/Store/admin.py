from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Product)
admin.site.register(Booth)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Color)
admin.site.register(Feature)
admin.site.register(Profile)


# Mix profile info and user info
class ProfileInLine(admin.StackedInline):
    model = Profile


# Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name' , 'email']
    inlines = [ProfileInLine]


#Un Register  the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)