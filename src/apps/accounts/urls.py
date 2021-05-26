from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import guest_register_view, login_view, register_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('register/guest/', guest_register_view, name='guest-register'),
]
