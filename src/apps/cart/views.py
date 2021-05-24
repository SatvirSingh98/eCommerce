from django.shortcuts import redirect, render

from apps.orders.models import Order
from apps.products.models import Product

from .models import Cart


def cart_home(request):
    cart_obj, _ = Cart.objects.create_or_get(request)  # from cart model manager.
    return render(request, 'cart/cart_home.html', {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')

    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print('Show message to user, product is gone?')
            return redirect('cart:home')
        cart_obj, _ = Cart.objects.create_or_get(request)

        # this is how to add into ManyToManyField
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_id)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()

    return redirect('cart:home')


def checkout(request):
    # from cart model manager.
    cart_obj, cart_created = Cart.objects.create_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    else:
        order_obj, _ = Order.objects.get_or_create(cart=cart_obj)
    return render(request, 'cart/checkout.html', {'object': order_obj})
