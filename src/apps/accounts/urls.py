from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import login_page, register_page

app_name = 'accounts'

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_page, name='register'),
]
