from django.urls import path

from .views import home

app_name = 'cart'

urlpatterns = [
    path('', home, name='cart-list'),
]
