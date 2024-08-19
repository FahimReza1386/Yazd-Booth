from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name='Home'),
    path('like-booth/', views.Like_Booth, name='Like_Booth'),
    path('check_like/', views.Check_Like, name='Check_Like'),
    path('about/', views.About, name='About'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('register/', views.Register, name='Register'),
    path('update_user/', views.Update_User, name='Update_User'),
    path('update_password/', views.Update_Password, name='Update_Password'),
    path('update_info/', views.Update_Info, name='Update_Info'),
    path('product/<int:id>', views.Product_Page, name='Product'),
    path('category/<str:foo>', views.Category_Page, name='Category'),
    path('Customer_userPanel/', views.Customer_UserPanel, name='Customer_UserPanel'),
    path('search/', views.Home, name='Search'),
]