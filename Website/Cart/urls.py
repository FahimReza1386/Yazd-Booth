from django.urls import path
from . import views

urlpatterns = [
    path('', views.Cart_Summary, name='Cart_Summary'),
    path('add/', views.Cart_Add , name='Cart_Add'),
    path('delete/', views.Cart_Delete, name='Cart_Delete'),
    path('update/', views.Cart_Update, name='Cart_Update'),
]