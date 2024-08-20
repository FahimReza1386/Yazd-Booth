from django.urls import path
from . import views



urlpatterns = [
    path('', views.Test, name='Test'),
    path('checkout/', views.CheckOut_Order, name='CheckOut_Order'),
]