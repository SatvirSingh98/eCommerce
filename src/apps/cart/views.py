from django.shortcuts import redirect, render

from apps.accounts.forms import GuestForm, LoginForm
from apps.addresses.forms import AddressForm
from apps.addresses.models import Address
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

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id')
    shipping_address_id = request.session.get('shipping_address_id')
    address_qs = None

    # from billing model manager
    billing_profile, _ = BillingProfile.objects.create_or_get(request)

    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        # if we want to choose specific address
        # shipping_address_qs = address_qs.filter(address_type='shipping')
        # billing_address_qs = address_qs.filter(address_type='billing')

        # from orders model manager.
        order_obj, _ = Order.objects.create_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()

        if request.method == 'POST':
            is_done = order_obj.checkout_success()
            if is_done:
                order_obj.order_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                return redirect('/cart/success')

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
    }
    return render(request, 'cart/checkout.html', context)
