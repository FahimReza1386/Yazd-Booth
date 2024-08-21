from django.urls import path
from . import views



urlpatterns = [
    path('checkout/', views.CheckOut_Order, name='CheckOut_Order'),
    path('billing_info/', views.Billing_Info, name='Billing_Info'),
    path('process_order/', views.Process_Order, name='Process_Order'),
]