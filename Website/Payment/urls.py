from django.urls import path
from . import views



urlpatterns = [
    path('checkout/', views.CheckOut_Order, name='CheckOut_Order'),
    path('billing_info/', views.Billing_Info, name='Billing_Info'),
    path('process_order/', views.Process_Order, name='Process_Order'),
    path('shipped_dash/', views.Shipped_Dash, name='Shipped_Dash'),
    path('not_shipped_dash/', views.Not_Shipped_Dash, name='Not_Shipped_Dash'),
    path('order/<int:id>', views.Order_Page , name='Order_Page'),
]