from django.contrib import admin
from .models import ShippingAddress,Order,OrderItem

# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


# Create an OrderItem Inline

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInline]

# UnRegister Order Model
admin.site.unregister(Order)

# re-Register out Order and OrderAdmin
admin.site.register(Order,OrderAdmin)