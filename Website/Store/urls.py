from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home, name='Home'),
    path('about/', views.About, name='About'),
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('register/', views.Register, name='Register'),
    path('product/<int:id>', views.Product_Page, name='Product'),
    path('category/<str:foo>', views.Category_Page, name='Category'),
]