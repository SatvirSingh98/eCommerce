from django.urls import path

from .views import cart_home, cart_update, checkout, checkout_success

app_name = 'cart'

urlpatterns = [
    path('', cart_home, name='home'),
    path('update/', cart_update, name='update'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/success/', checkout_success, name='checkout-success'),
]
