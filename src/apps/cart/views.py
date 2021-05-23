from django.shortcuts import render

from .models import Cart


def home(request):
    cart_obj, _ = Cart.objects.create_or_get(request)  # from cart model manager.
    return render(request, 'cart/home.html', {'cart_id': cart_obj.id})
