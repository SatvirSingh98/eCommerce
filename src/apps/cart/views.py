from django.shortcuts import redirect, render

from apps.accounts.forms import GuestForm, LoginForm
from apps.accounts.models import GuestEmail
from apps.billing.models import BillingProfile
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

    user = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')

    if user.is_authenticated:
        billing_profile, _ = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, _ = BillingProfile.objects.get_or_create(email=guest_email)

    if billing_profile is not None:
        # from orders model manager.
        order_obj, _ = Order.objects.create_or_get(billing_profile, cart_obj)

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form
    }
    return render(request, 'cart/checkout.html', context)
