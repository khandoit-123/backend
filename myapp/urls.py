from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('add-to-cart-all', views.add_to_cart_all, name='add_to_cart_all'),
    path('cooking', views.cooking, name='cooking'),
    path('', views.home, name="home"),
    path('reservation', views.reservation, name='reservation'),
    path('order', views.order, name='order'),
    path('register', views.register, name='register'),
    path('chef', views.chef, name='chef'),
    path('checkout', views.checkout, name='checkout'),
]